Overview
========

This project demonstrates how to integrate Azure Active Directory B2C in a Python web application. It is based on https://github.com/Azure-Samples/ms-identity-python-webapp.git

- Prerequisites
- Infrastructure Setup
- Configure Development Environment

Prerequisites
=============

- `Create and AD B2C Tenant <https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant>`_

Infra Setup
===========

- Register the python web app in the B2C tenant.
- Create User Flows for Authenticating B2C Users in the web app
- Create an App service to host the Web App

Register Application
--------------------

You'll need to save the registered app_id and password for development or deploying

.. code-block:: bash

    # Optional Load .env vars
    # set -o allexport; source .env; set +o allexport
    app_name=python-b2c-app

    # constants
    ms_graph_api_id="00000003-0000-0000-c000-000000000000"
    openid_permission="37f7f235-527c-4136-accd-4a02d197296e"
    offline_access_permission="7427e0e9-2fba-42fe-b0c0-848c9e6a8182"
    app_secret_name=py_webapp_client_secret

    az login --tenant $B2C_TENANT.onmicrosoft.com --allow-no-subscriptions

    # Azure CLI Steps
    # create app
    app_id=$(az ad app create --display-name $app_name --web-redirect-uris "https://jwt.ms" --query id -o tsv)
    # Save app_id to .env CLIENT_ID
    # Configure permissions
    az ad app permission add --id $app_id --api $ms_graph_api_id --api-permissions $openid_permission=Scope $offline_access_permission=Scope
    az ad app permission admin-consent --id $app_id
    # Create Client secret (application password)
    az ad app credential reset --id $app_id --display-name $app_secret_name --year 2
    # Save password to .env CLIENT_SECRET
    # Manually set Implicit grant and hyubrid flows for testing with https://jwt.ms/

    # Azure Graph Steps
    # create app
    # az rest --method POST --uri "https://graph.microsoft.com/v1.0/applications/" --body "{'displayName':'$app_name'}"
    # app_id=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/applications?\$filter=displayName eq '$app_name'" | jq .value[0].id -r)
    # az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/$app_id" --body '{"web":{"redirectUris":["https://jwt.ms"]}}'
    # Configure permissions
    # az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/$app_id" --body '{"requiredResourceAccess":[{"resourceAccess": [{"id": "$openid_permission","type": "Scope"},{"id": "$offline_access_permission","type": "Scope"}],"resourceAppId": "$ms_graph_api_id"}]}'
    # Create Client secret (application password)
    # az rest --method POST --uri "https://graph.microsoft.com/v1.0/applications/$app_id/addPassword" --body "{'passwordCredential': {'displayName': '$app_secret_name'}}"


To get available permissions for Microsoft Graph API run:

.. code-block:: bash

    # appRoles correspond to Role in --api-permissions
    az ad sp show --id $ms_graph_api_id | jq '.appRoles[] | {displayName,id}'

    # oauth2PermissionScopes correspond to Scope in --api-permissions
    az ad sp show --id $ms_graph_api_id | jq '.oauth2PermissionScopes[] | {adminConsentDisplayName,type,id}'

To auto-append .env file with CLIENT_ID and CLIENT_SECRET use:

.. code-block:: bash

    az ad app credential reset --id $app_id --display-name $app_secret_name --year 2 | jq -r '.password' | awk '{printf "APP_CLIENT_SECRET=%s", $1;}' >> .env

Create user Flows
-----------------

- A combined Sign in and sign up user flow, such as susi. This user flow also supports the Forgot your password experience.
- A Profile editing user flow, such as edit_profile.

Create App Service
-------------------

.. code-block:: bash

    # Optional Load .env vars
    # set -o allexport; source .env; set +o allexport

    az login --tenant $TENANT_NAME.onmicrosoft.com

    let "randomIdentifier=$RANDOM*$RANDOM"
    rg_region=eastus
    rg_name=LMS-WebApp-RG

    app_plan="asp-lms-$randomIdentifier"
    webapp="wa-lms-$randomIdentifier"

    # Create a resource group.
    az group create --name $rg_name --location "$rg_region"

    # Create an App Service plan in `FREE` tier.
    az appservice plan create --name $app_plan --resource-group $rg_name --sku FREE --location $rg_region --is-linux

    # Create a web app.
    az webapp create --name $webapp --resource-group $rg_name --plan $app_plan --runtime PYTHON:3.9
    az webapp auth update --resource-group $rg_name --name $webapp --enabled false



Configure dev environment
=========================

Setup your dev environment by creating a virtual environment

.. code-block:: bash

    # Windows
    # virtualenv \path\to\.venv -p path\to\specific_version_python.exe
    # C:\Users\!Admin\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
    # .venv\scripts\activate

    # Linux
    # virtualenv .venv /usr/local/bin/python3.10
    # python3.10 -m venv .venv
    # python3 -m venv .venv
    python3 -m venv .venv
    source .venv/bin/activate

    # Update pip
    python -m pip install --upgrade pip

    deactivate

Install dependencies and configure ``local.env``.

.. code-block:: bash

    # Install dependencies
    pip install -r requirements_dev.txt

    # Replace settings in local.env
    cp example.env .env

    # Optional - Load .env into bash ENV vars
    # set -o allexport; source .env; set +o allexport

Install locally for development and enable pre-commit scripts.

.. code-block:: bash

    pip install --editable .

    pre-commit install

Style Guidelines
----------------

This project enforces quite strict `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 (Docstring Conventions) <https://www.python.org/dev/peps/pep-0257/>`_ compliance on all code submitted.

We use `Black <https://github.com/psf/black>`_ for uncompromised code formatting.

Summary of the most relevant points:

- Comments should be full sentences and end with a period.
- `Imports <https://www.python.org/dev/peps/pep-0008/#imports>`_  should be ordered.
- Constants and the content of lists and dictionaries should be in alphabetical order.
- It is advisable to adjust IDE or editor settings to match those requirements.

Use new style string formatting
-------------------------------

Prefer `f-strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`_ over ``%`` or ``str.format``.

.. code-block:: python

    # New
    f"{some_value} {some_other_value}"
    # Old, wrong
    "{} {}".format("New", "style")
    "%s %s" % ("Old", "style")

One exception is for logging which uses the percentage formatting. This is to avoid formatting the log message when it is suppressed.

.. code-block:: python

    _LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)

Testing
--------
You'll need to install the test dependencies and project into your Python environment:

.. code-block:: bash

    pip3 install -r requirements_dev.txt
    pip install --editable .

Now that you have all test dependencies installed, you can run tests on the project:

.. code-block:: bash

    isort .
    codespell  --skip="./.*,*.csv,*.json,*.pyc,./docs/_build/*,./htmlcov/*"
    black *.py
    flake8 .
    pylint *.py
    rstcheck README.rst
    pydocstyle *.py

Deploy Web App
--------------

Deploy web app to app service.

.. code-block:: bash

    gitrepo=https://github.com/briglx/python-b2c-app

    # Deploy code from a public GitHub repository.
    az webapp deployment source config --name $webapp --resource-group $rg_name \
    --repo-url $gitrepo --branch master --manual-integration

    # Use curl to see the web app.
    site="http://$webapp.azurewebsites.net"
    echo $site
    curl "$site"


References
==========

- B2C Auth in Python app https://docs.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app?tabs=windows
- Register an app in AAD B2C https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-applications?tabs=app-reg-ga
- Example Sign in Flow https://docs.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy?pivots=b2c-user-flow
- Azure Graph API create an app https://docs.microsoft.com/en-us/graph/api/application-post-applications?view=graph-rest-1.0&tabs=http
