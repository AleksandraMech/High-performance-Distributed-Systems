import pika
import json
import cfg  # Assuming you have the necessary RabbitMQ configuration in cfg

def send_order_to_rabbitmq(order_data):
    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=cfg.rabbitmq_host, port=cfg.rabbitmq_port)
        )
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='order_queue', durable=True)

        # Send order data to the queue
        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=json.dumps(order_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        print("Order sent to RabbitMQ")
        connection.close()
        return True
    except Exception as e:
        print(f"Failed to send order to RabbitMQ: {e}")
        return False
