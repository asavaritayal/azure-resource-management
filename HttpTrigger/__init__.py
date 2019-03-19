import logging
import os

import azure.functions as func
import datetime 
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
import azure.mgmt.resource.resources.models
from azure.common.credentials import ServicePrincipalCredentials

credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )

resource_client = ResourceManagementClient(credentials, os.environ['AZURE_SUBSCRIPTION_ID'])
   
compute_client = ComputeManagementClient(credentials, os.environ['AZURE_SUBSCRIPTION_ID'])


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    rgList = resource_client.resource_groups.list()

    for rg in rgList:
        print_item (rg)
        # In case there are no tags or no tag with 'Project' name, tag the resource group as unknown and set an expiration date
        if rg.tags == None:
            expDate = str(datetime.date.today() + datetime.timedelta(31))
            patched_tags = rg.tags or {}
            patched_tags['Project'] = 'Unknown'
            patched_tags['ExpirationDate'] = expDate
            params_patch = azure.mgmt.resource.resources.models.ResourceGroupPatchable(tags=patched_tags)
            resource_client.resource_groups.update (rg.name, params_patch)
            logging.info("Tag: {} as project Unknown with an expiration date ".format(rg.name))

        elif 'Project' not in rg.tags:
            expDate = str(datetime.date.today() + datetime.timedelta(31))
            patched_tags = rg.tags or {}
            patched_tags['Project'] = 'Unknown'
            patched_tags['ExpirationDate'] = expDate
            params_patch = azure.mgmt.resource.resources.models.ResourceGroupPatchable(tags=patched_tags)
            resource_client.resource_groups.update (rg.name, params_patch)
            logging.info("Tag: {} as project Unknown with an expiration date ".format(rg.name))

        elif rg.tags['Project'] == "Unknown":
            if 'ExpirationDate' not in rg.tags or rg.tags['ExpirationDate']== '' :
                expDate = str(datetime.date.today() + datetime.timedelta(31))
                patched_tags = rg.tags or {}
                patched_tags['ExpirationDate'] = expDate
                params_patch = azure.mgmt.resource.resources.models.ResourceGroupPatchable(tags=patched_tags)
                resource_client.resource_groups.update (rg.name, params_patch)
                logging.info("Tag: {} as project Unknown with an expiration date ".format(rg.name))

        else:           
            logging.info("No need to tag {} ".format(rg.name))

    return func.HttpResponse(f"ResourceIterator - Completed")

def print_item(group):
    """Print a ResourceGroup instance."""
    logging.info("\tName: {}".format(group.name))
    logging.info("\tId: {}".format(group.id))
    logging.info("\tLocation: {}".format(group.location))
    logging.info("\tTags: {}".format(group.tags))
    print_properties(group.properties)


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        logging.info("\tProperties:")
        logging.info("\t\tProvisioning State: {}".format(props.provisioning_state))
    logging.info("\n\n")
