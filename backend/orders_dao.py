from datetime import datetime
from sql_connection import get_sql_connection


def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table
    order_query = ("INSERT INTO orders "
                   "(customer_name, total, datetime) "
                   "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid  # Get the ID of the newly inserted order

    # Insert into order_details table
    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price) "
                           "VALUES (%s, %s, %s, %s)")

    # Prepare data for executemany()
    order_details_data = [
        (order_id, int(detail['product_id']), float(detail['quantity']), float(detail['total_price']))
        for detail in order['order_details']
    ]

    # Execute multiple insertions at once
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()
    cursor.close()

    return order_id


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    # Join orders and products to get product information
    query = """
    SELECT order_details.order_id, order_details.quantity, order_details.total_price, 
           products.name, products.price_per_unit 
    FROM order_details 
    LEFT JOIN products ON order_details.product_id = products.product_id 
    WHERE order_details.order_id = %s
    """
    data = (order_id,)

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records


def get_all_orders(connection):
    cursor = connection.cursor()

    # Fetch all orders
    query = "SELECT * FROM orders"
    cursor.execute(query)

    orders = []
    for (order_id, customer_name, total, dt) in cursor:
        orders.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt
        })

    cursor.close()

    # Fetch order details for each order
    for order in orders:
        order['order_details'] = get_order_details(connection, order['order_id'])

    return orders


if __name__ == '__main__':
    connection = get_sql_connection()

    # Fetch all orders and their details
    print(get_all_orders(connection))

