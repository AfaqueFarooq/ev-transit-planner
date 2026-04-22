from dotenv import load_dotenv
import os

load_dotenv()

VBB_BASE_URL = os.getenv("VBB_BASE_URL", "https://vb.vbb.transport.rest/")
APP_NAME = os.getenv("APP_NAME", "EV Transit Planner")
DEBUG = os.getenv("DEBUG", "True")
CHARGETRIP_URL = os.getenv("CHARGETRIP_URL", "https://api.chargetrip.io/graphql")
CHARGETRIP_CLIENT_ID = os.getenv("CHARGETRIP_CLIENT_ID", "")
CHARGETRIP_APP_ID = os.getenv("CHARGETRIP_APP_ID", "")