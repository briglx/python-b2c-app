# Setup using Graph API


Register Application
--------------------

Register the application with the B2C tenant to provide authentication for B2C users.

Save the registered ``app_id`` and ``password`` for development or deploying

.. code-block:: bash

    # Optional Load .env vars
    # set -o allexport; source .env; set +o allexport
    app_name=python-b2c-app

    # constants
    ms_graph_api_id="00000003-0000-0000-c000-000000000000"
    ms_graph_openid_permission="37f7f235-527c-4136-accd-4a02d197296e"
    ms_graph_offline_access_permission="7427e0e9-2fba-42fe-b0c0-848c9e6a8182"
    app_secret_name=py_webapp_client_secret

    az login --tenant $B2C_TENANT.onmicrosoft.com --allow-no-subscriptions

    # create app
    az rest --method POST --uri "https://graph.microsoft.com/v1.0/applications/" --body "{'displayName':'$app_name'}"
    app_id=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/applications?\$filter=displayName eq '$app_name'" | jq .value[0].id -r)
    # Save app_id to .env CLIENT_ID

    # configure authentication
    az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/$app_id" --body '{"web":{"redirectUris":["https://jwt.ms", "http://127.0.0.1:5000/getAToken"]}}'

    # manually set implicit grant and hybrid flow (Optional)
    # select both access tokens and id tokens when testing with https://jwt.ms/.
    # found on application authentication page

    # create client secret (application password)
    az rest --method POST --uri "https://graph.microsoft.com/v1.0/applications/$app_id/addPassword" --body "{'passwordCredential': {'displayName': '$app_secret_name'}}"
    # Save password to .env CLIENT_SECRET

    # configure api permissions
    az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/$app_id" --body '{"requiredResourceAccess":[{"resourceAccess": [{"id": "$ms_graph_openid_permission","type": "Scope"},{"id": "$ms_graph_offline_access_permission","type": "Scope"}],"resourceAppId": "$ms_graph_api_id"}]}'
