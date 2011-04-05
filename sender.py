import sys
import amqplib.client_0_8 as amqp

def main():
    msg_body = ''.join(sys.argv[1:])

    conn = amqp.Connection()
    ch = conn.channel()
    ch.access_request('/data', active=True, write=True)

    ch.exchange_declare('myfan', 'fanout', auto_delete=True)

    msg = amqp.Message(msg_body, content_type='text/plain', application_headers={'foo': 7, 'bar': 'baz'})

    ch.basic_publish(msg, 'myfan')

    ch.close()
    conn.close()

if __name__ == '__main__':
    main()
