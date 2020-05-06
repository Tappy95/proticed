import nsq


def handler(message):
    print(message)
    return True


r = nsq.Reader(message_handler=handler,
               lookupd_http_addresses=['http://47.112.96.218:4161'],
               topic='ebay_analysis_report.product', channel='test', lookupd_poll_interval=15)
nsq.run()
