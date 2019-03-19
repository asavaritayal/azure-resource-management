Python Function App to automate resource cleanup in Azure.

### Prerequisites

To use this sample:

- Install [Python 3.6](https://www.python.org/downloads/)
- Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) version 2.x or later.
- Install [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2) version 2.2.70 or later (requires .NET Core 2.x SDK).

### Download the sample

In a terminal window, run the following commands to clone the sample application to your local machine, and navigate to the directory with the sample code.

```bash
git clone https://github.com/asavaritayal/azure-resource-management.git
cd azure-resource-management
```

### Create and activate a virtual environment

To work with an Python Azure Function project, it is required that you work in a Python 3.6 virtual environment. Run the following commands to create and activate a virtual environment named .env.

```bash
# In Bash
python3.6 -m venv .env
source .env/bin/activate

# In PowerShell
py -3.6 -m venv .env
.env\scripts\activate
```

### Install dependencies

The names and versions of the required packages are already listed in the `requirements.txt` file. Use the following command to install these dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Create a Service Principal

To grant your Function App the permission to manage resources in a specific subscription in Azure, you will need to create a Service Principal using the following commands:

```bash
az account set --subscription="SUBSCRIPTION_ID"
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/SUBSCRIPTION_ID"
```

This command will output 5 values:

```
{
  "appId": "00000000-0000-0000-0000-000000000000",
  "displayName": "azure-cli-2017-06-05-10-41-15",
  "name": "http://azure-cli-2017-06-05-10-41-15",
  "password": "0000-0000-0000-0000-000000000000",
  "tenant": "00000000-0000-0000-0000-000000000000"
}
```

### Add local settings

Use the following commands to configure the required secrets as local settings for your application:

```bash
func settings add AZURE_SUBSCRIPTION_ID {SUBSCRIPTION_ID}
func settings add AZURE_CLIENT_ID {appId}
func settings add AZURE_CLIENT_SECRET {password}
func settings add AZURE_TENANT_ID {tenant}
```

### Test

Use the following command to run the Functions host locally.

```bash
func host start
```

Trigger the function from the command line using curl in a new terminal window:

```bash
curl -w '\n' http://localhost:7071/api/HttpTrigger
```

### Publish to Azure

Using the Azure Functions Core Tools, run the following command. Replace <APP_NAME> with the name of your Linux Function App.

```bash
func azure functionapp publish <APP_NAME> --publish-local-settings --build-native-deps
```