import os
import sys

# is open cross domain
OPEN_CROSS_DOMAIN = True if os.getenv("STAGE", "prod") == "dev" else False

DEFAULT_BIND_HOST = "0.0.0.0" if sys.platform != "win32" else "127.0.0.1"

# api.py server
API_SERVER = {
    "host": DEFAULT_BIND_HOST,
    "port": 7861,
}
