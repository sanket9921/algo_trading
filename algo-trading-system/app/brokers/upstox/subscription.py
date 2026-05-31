import json

from app.brokers.upstox.models import MarketSubscription


def build_subscription_payload(
    subscription: MarketSubscription,
) -> str:
    payload = {
        "guid": "algo-trading-system",
        "method": "sub",
        "data": {
            "mode": subscription.mode,
            "instrumentKeys": subscription.instrument_keys,
        },
    }

    return json.dumps(payload)