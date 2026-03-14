

def _to_event_ts_ms(event: dict) -> int:
    raw_ts = int(event.get("timestamp") or 0)
    if raw_ts <= 0:
        import time
        return int(time.time() * 1000)
    if raw_ts < 10_000_000_000:
        return raw_ts * 1000
    return raw_ts


def normalize_auction(event):
    item = event["data"]["item"]
    event_ts_ms = _to_event_ts_ms(event)

    final_bid = float(event["data"]["finalBid"])
    amount = float(event["data"]["amount"])

    return {
        "event_type": "auction",
        "item_type": item["type"],
        "item_name": item.get("name"),
        "snbt": item.get("snbt", "{}"),
        "quantity": amount,
        "unit_price": final_bid,
        "total_price": final_bid * amount,
        "currency_amount": final_bid * amount,
        "shop_x": None,
        "shop_y": None,
        "shop_z": None,
        "shop_world": None,
        "transaction_type": "auctionComplete",
        "created_at": event_ts_ms,
    }


def normalize_shop_transaction(event):
    data = event["data"]
    loc = data["location"]
    item = data["item"]
    event_ts_ms = _to_event_ts_ms(event)

    return {
        "event_type": "shop",
        "item_type": item["type"],
        "item_name": item.get("name"),
        "snbt": item.get("snbt", "{}"),
        "quantity": data["totalAmount"],
        "unit_price": data["currencyAmount"] / data["totalAmount"] if float(data["totalAmount"] or 0) > 0 else 0.0,
        "total_price": data["currencyAmount"],
        "currency_amount": data["currencyAmount"],
        "shop_x": loc["x"],
        "shop_y": loc["y"],
        "shop_z": loc["z"],
        "shop_world": loc["world"],
        "transaction_type": data["type"],
        "created_at": event_ts_ms,
    }
