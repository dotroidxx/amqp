import amqplib.client_0_8 as amqp

def callback(msg):
    for key, val in msg.properties.items():
        print '%s: %s' % (key, str(val))
    for key, val in msg.delivery_info.items():
        print '> %s: %s' % (key, str(val))

    print ''
    print msg.body
    print '--------------------'

    msg.channel.basic_ack(msg.delivery_tag)

    if msg.body == 'quit':
        msg.channel.basic_cancel(msg.consumer_tag)

def main():
    conn = amqp.Connection()
    ch = conn.channel()
    ch.access_request('/data', active=True, read=True)

    ch.exchange_declare('myfan', 'fanout', auto_delete=True)

    qname, _, _ = ch.queue_declare()

    ch.queue_bind(qname, 'myfan')
    ch.basic_consume(qname, callback=callback)

    while ch.callbacks:
        ch.wait()

    ch.close()
    conn.close()

if __name__ == '__main__':
    main()
