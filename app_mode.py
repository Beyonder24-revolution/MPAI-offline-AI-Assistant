#online mode
ONLINE_KNOWLEDGE = True
# core/app_mode.py

APP_MODE = "demo"  
# change to "secure" later

def is_demo():
    return APP_MODE == "demo"

def is_secure():
    return APP_MODE == "secure"
