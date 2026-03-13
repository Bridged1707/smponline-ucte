import time


def normalize_shop(shop):

    item = shop["item"]
    loc = shop["location"]
    owner = shop["owner"]

    return {

        "id": int(shop["id"]),

        "owner_name": owner.get("name"),
        "owner_uuid": owner.get("uuid"),

        "world": loc.get("world"),
        "x": int(loc.get("x")),
        "y": int(loc.get("y")),
        "z": int(loc.get("z")),

        "shop_type": shop.get("type"),
        "price": float(shop.get("price") or 0),
        "remaining": int(shop.get("remaining") or 0),

        "item_type": item.get("type"),
        "item_name": item.get("name") or item.get("type"),
        "item_quantity": int(item.get("quantity") or 1),

        "snbt": item.get("snbt") or "{}",

        "last_seen": int(time.time())
    }