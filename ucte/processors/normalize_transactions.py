import time


def normalize_auction(event):

    item = event["data"]["item"]

    return {

        "event_type": "auction",

        "item_type": item["type"],
        "item_name": item.get("name"),
        "snbt": item.get("snbt", "{}"),

        "quantity": event["data"]["amount"],
        "unit_price": event["data"]["finalBid"],
        "total_price": event["data"]["finalBid"] * event["data"]["amount"],

        "currency_amount": event["data"]["finalBid"],

        "shop_x": None,
        "shop_y": None,
        "shop_z": None,
        "shop_world": None,

        "transaction_type": "auction",

        "created_at": int(time.time())
    }


def normalize_shop_transaction(event):

    data = event["data"]
    loc = data["location"]
    item = data["item"]

    return {

        "event_type": "shop",

        "item_type": item["type"],
        "item_name": None,
        "snbt": item.get("snbt", "{}"),

        "quantity": data["totalAmount"],
        "unit_price": data["itemPrice"],
        "total_price": data["currencyAmount"],

        "currency_amount": data["currencyAmount"],

        "shop_x": loc["x"],
        "shop_y": loc["y"],
        "shop_z": loc["z"],
        "shop_world": loc["world"],

        "transaction_type": data["type"],

        "created_at": int(time.time() * 1000)
    }