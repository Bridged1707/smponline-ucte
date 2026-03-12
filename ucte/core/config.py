import os
from dotenv import load_dotenv

load_dotenv()

# UTDB API
UTDB_API_URL = os.getenv("UTDB_API_URL")

# Shop snapshot API
SHOP_ENDPOINT = os.getenv(
    "SHOP_ENDPOINT",
    "https://smponline-api.callmecarson.live/quickshop/v1/getAllShops"
)

SHOP_SYNC_INTERVAL = int(
    os.getenv("SHOP_SYNC_INTERVAL", "120")
)

# Economy websocket
ECONOMY_WS = os.getenv(
    "ECONOMY_WS",
    "wss://smponline-api.callmecarson.live/economy/v1/ws"
)

ECONOMY_WS_RECONNECT_DELAY = int(
    os.getenv("ECONOMY_WS_RECONNECT_DELAY", "5")
)

# Required by API
USER_AGENT = os.getenv(
    "USER_AGENT",
    "smponline-ucte/1.0"
)