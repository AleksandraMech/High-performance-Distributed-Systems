import pika
import json
import cfg  # Assuming you have the necessary RabbitMQ configuration in cfg

def receive_all_orders_from_rabbitmq():
    orders = []
    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=cfg.rabbitmq_host, port=cfg.rabbitmq_port)
        )
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='order_queue', durable=True)

        while True:
            method_frame, header_frame, body = channel.basic_get(queue='order_queue', auto_ack=True)
            if method_frame:
                order_data = json.loads(body)
                orders.append(order_data)
            else:
                break

        connection.close()
    except Exception as e:
        print(f"Failed to receive orders from RabbitMQ: {e}")

    return orders
