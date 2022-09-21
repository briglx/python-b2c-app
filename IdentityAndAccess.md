# Identity and Access

Notes to configure SSO for domain based users.

Goal: Allow user@example.com to sso into my application hosted at test_tenant using b2c tenant test_tenant_guest


# Terms

| Term | Definition |
|------|-------------|
| JWT token |        |
| OpenID Connect (OIDC) | Extends the OAuth 2.0 authz protocol for use as an authn protocol |
| ID token | OIDC token to vaerify identity of user and obtain basic profile info |
| access token | use access tokens to access resources that are secured by an authorizaiton server |
|

# Notes

Users can have multiple itentities

Identity Providers
- External Identities (AAD and AAD B2C)
    - BuiltInIdentityProvider
        - AAD Tenant
        - B2B (AAD, Microsoft account(MSA), email one-time passcode (EmailOTP))
    - SocialIdentityProvider (AAD and AAD B2C)
        - B2B (Google or Facebook)
        - B2C (Microsoft, Google, Facebook, Amazon, LinkedIn, Twitter, preview: Weibo, QQ, WeChat, Github)
    - AppleManagedIdentityProvier (AAD B2C)
- Domain Based External Identities (AAD)
    - samlOrWsFedProvider (SAML, WS-Fed)
    - internalDomainFederation - Federation with AAD




Local Accounts
- Email Signup
- User ID Signup
- None


Example User with Different Identities

```json
    {
      "displayName": "TestUser2 TestUser2Last",
      "id": "0aea7395-29e8-481d-a7f3-01f4a058fdb3",
      "identities": [
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "testuser1@example.com",
          "signInType": "emailAddress"
        },
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "65a4dbe2-72a3-4f9c-8037-d19664faab48@example_b2c_tenant.onexample.com",
          "signInType": "userPrincipalName"
        }
      ],
      "userPrincipalName": "65a4dbe2-72a3-4f9c-8037-d19664faab48@example_b2c_tenant.onexample.com",
      "userType": "Member"
    },
    {
      "displayName": "TestUser AtExample",
      "id": "2fb2df42-8ea7-41be-9fdd-3fbf24009d05",
      "identities": [
        {
          "issuer": "ExternalAzureAD",
          "issuerAssignedId": null,
          "signInType": "federated"
        },
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "TestUser.AtExample_example.com#EXT#@example_b2c_tenant.onexample.com",
          "signInType": "userPrincipalName"
        }
      ],
      "userPrincipalName": "TestUser.AtExample_example.com#EXT#@example_b2c_tenant.onexample.com",
      "userType": "Member"
    },
    {
      "displayName": "TestUser3",
      "id": "abcf647e-0e5c-40c1-a6e8-9a0b74b5cb34",
      "identities": [
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "testuser3@example.com",
          "signInType": "emailAddress"
        },
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "abcf647e-0e5c-40c1-a6e8-9a0b74b5cb34@example_b2c_tenant.onexample.com",
          "signInType": "userPrincipalName"
        }
      ],
      "userPrincipalName": "abcf647e-0e5c-40c1-a6e8-9a0b74b5cb34@example_b2c_tenant.onexample.com",
      "userType": "Member"
    },

    {
      "displayName": "TestUserlx",
      "id": "bf794b4a-daf4-4b2e-aa30-d55b826031e5",
      "identities": [
        {
          "issuer": "github.com",
          "issuerAssignedId": "1304774",
          "signInType": "federated"
        },
        {
          "issuer": "example_b2c_tenant.onexample.com",
          "issuerAssignedId": "cpim_cc2be20e-74ed-4484-926f-8e76b4dc5cf6@example_b2c_tenant.onexample.com",
          "signInType": "userPrincipalName"
        }
      ],
      "userPrincipalName": "cpim_cc2be20e-74ed-4484-926f-8e76b4dc5cf6@example_b2c_tenant.onexample.com",
      "userType": "Member"
    },

```

I was able to create an External Federated User Identity but can't use that identity to log into the application

```bash

az rest --method POST --uri "https://graph.example.com/v1.0/invitations" --body '{"invitedUserEmailAddress": "example_user@example_tenant.onexample.com","inviteRedirectUrl": "https://wa-lms-150676709.azurewebsites.net"}"'

```

| User Type | Federated - GitHub    | email addr                    | Federated - Microsoft         | Federated - ExternalAzureAD |
|-----------|-----------------------|-------------------------------|-------------------------------|-----------------------------|
| Member    | TestUserlx success        |  testuser3@example.com success   |                               |                             |
| Guest     |                       |                               |  bkAtExample@example.com failed |   example_user@example_tenant.com  failed |



OpenID Connect Metadata

Discovery document path: /.well-known/openid-configuration
Authority: https://login.microsoftonline.com/{tenant_id}/v2.0

# Fetch OpenID metadata
Authority: https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/v2.0/.well-known/openid-configuration

```json
{"token_endpoint":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/oauth2/v2.0/token","token_endpoint_auth_methods_supported":["client_secret_post","private_key_jwt","client_secret_basic"],"jwks_uri":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/discovery/v2.0/keys","response_modes_supported":["query","fragment","form_post"],"subject_types_supported":["pairwise"],"id_token_signing_alg_values_supported":["RS256"],"response_types_supported":["code","id_token","code id_token","id_token token"],"scopes_supported":["openid","profile","email","offline_access"],"issuer":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/v2.0","request_uri_parameter_supported":false,"userinfo_endpoint":"https://graph.example.com/oidc/userinfo","authorization_endpoint":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/oauth2/v2.0/authorize","device_authorization_endpoint":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/oauth2/v2.0/devicecode","http_logout_supported":true,"frontchannel_logout_supported":true,"end_session_endpoint":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/oauth2/v2.0/logout","claims_supported":["sub","iss","cloud_instance_name","cloud_instance_host_name","cloud_graph_host_name","msgraph_host","aud","exp","iat","auth_time","acr","nonce","preferred_username","name","tid","ver","at_hash","c_hash","email"],"kerberos_endpoint":"https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/kerberos","tenant_region_scope":"NA","cloud_instance_name":"microsoftonline.com","cloud_graph_host_name":"graph.windows.net","msgraph_host":"graph.example.com","rbac_url":"https://pas.windows.net"}
```


# OpenID Connect Sign In

```bash

# Fetch metadata document

$tenant_id=$

wget -q -O - "https://login.microsoftonline.com/${tenant_id}/v2.0/.well-known/openid-configuration"

```



Debug Token
-----------

- Add redirect URI to golam app to postman

Call
```bash

curl --location --request GET 'https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/oauth2/v2.0/authorize?client_id=f8b136d6-9288-45a5-8eb8-aa6bd3a0c52e&response_type=id_token&redirect_uri=https%3A%2F%2Fjwt.ms&response_mode=fragment&scope=openid%20profile%20email&state=12345&nonce=678910'

```

Response
```json
{
  "typ": "JWT",
  "alg": "RS256",
  "kid": "2ZQpJ3UpbjAYXYGaXEJl8lV0TOI"
}.{
  "aud": "f8b136d6-9288-45a5-8eb8-aa6bd3a0c52e",
  "iss": "https://login.microsoftonline.com/8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe/v2.0",
  "iat": 1659463926,
  "nbf": 1659463926,
  "exp": 1659467826,
  "aio": "ATQAy/8TAAAA2Yqfd0RF4y8QnV7fUKr3ZxFgvnSAt/1PBgNg9oHbvQsGt2J3lInrwXXTFvhLT7+N",
  "name": "Test User 1",
  "nonce": "678910",
  "oid": "6e55bfcb-6184-411b-983b-6ed0e0f87d24",
  "preferred_username": "testuser1@goAtExample.com",
  "rh": "0.AXgAakF5jAZfWEC5Rxocx6tk_tY2sfiIkqVFjriqa9OgxS54AJw.",
  "sub": "jx0vDBsfHFU4GAdD-dIVxSrL0sqG7wCzsKb_u9sdApE",
  "tid": "8xxxxxxxa-5xx6-4xx8-bxx7-1xxxxxxxxxxe",
  "uti": "Ezn6_6C_CE-APtakpPh-AQ",
  "ver": "2.0"
}.[Signature]
```

# Create a custom login flow

Custom Policy was renamed to IDF

Create a custom flow
- Check if principal exists
- if yes map the identity

Base files have:
- Actions
- Claims (values)

See examples in https://dev.azure.com/CSECodeHub/_git/356104%20-%20UHG%20ProtectWell%20fka%20Return%20to%20WorkBack%20to%20Work
