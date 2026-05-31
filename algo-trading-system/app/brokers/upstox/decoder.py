from app.brokers.upstox.proto import MarketDataFeed_pb2


def decode_market_feed(buffer: bytes):
    feed_response = MarketDataFeed_pb2.FeedResponse()

    feed_response.ParseFromString(buffer)

    return feed_response