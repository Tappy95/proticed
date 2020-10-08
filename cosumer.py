import nsq


def handler(message):
    print(message.body)
    return True


r = nsq.Reader(message_handler=handler,
               lookupd_http_addresses=['192.168.6.198:4161'],
               topic='amazon_minor_language_asin_info', channel='test', lookupd_poll_interval=15)
nsq.run()
