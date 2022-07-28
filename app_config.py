"""Flask app config file."""
import os

# Load env variables
B2C_TENANT = os.getenv("B2C_TENANT")
CLIENT_ID = os.getenv("APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET")

if not B2C_TENANT:
    raise ValueError("Need to define B2C_TENANT environment variable")
if not CLIENT_ID:
    raise ValueError("Need to define APP_CLIENT_ID environment variable")
if not CLIENT_SECRET:
    raise ValueError("Need to define APP_CLIENT_SECRET environment variable")

SIGNUP_SIGNIN_USER_FLOW = "B2C_1_susi"
EDIT_PROFILE_USER_FLOW = "B2C_1_edit_profile"
REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

SCOPE = []
SESSION_TYPE = (
    "filesystem"  # Specifies the token cache should be stored in server-side session
)

AUTHORITY_TEMPLATE = (
    "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"
)
AUTHORITY = AUTHORITY_TEMPLATE.format(
    tenant=B2C_TENANT, user_flow=SIGNUP_SIGNIN_USER_FLOW
)
B2C_PROFILE_AUTHORITY = AUTHORITY_TEMPLATE.format(
    tenant=B2C_TENANT, user_flow=EDIT_PROFILE_USER_FLOW
)
