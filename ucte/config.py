import os

UTCON_URL = os.getenv("UTCON_URL", "http://10.1.0.102:8080")

SMP_API_BASE = "https://smponline-api.callmecarson.live"
SMP_WS_URL = "wss://smponline-api.callmecarson.live/economy/v1/ws"

SHOP_SYNC_INTERVAL = 3000

TRANSACTION_BATCH_SIZE = 100
SHOP_BATCH_SIZE = 500
