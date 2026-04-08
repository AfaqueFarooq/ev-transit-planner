from dotenv import load_dotenv
import os

load_dotenv()

VBB_BASE_URL = os.getenv("VBB_BASE_URL", "https://vbb.transport.rest/") 
APP_NAME = os.getenv("APP_NAME", "EV Transit Planner")
DEBUG = os.getenv("DEBUG", "True")