from sql_connection import get_sql_connection


# Get all products
def get_all_products(connection):
    cursor = connection.cursor()

    query = ("SELECT products.product_id, products.name, "
             "products.uom_id, products.price_per_unit, uom.uom_name "
             "FROM products "
             "INNER JOIN uom ON products.uom_id = uom.uom_id;")

    cursor.execute(query)
    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })

    cursor.close()  # Close cursor after use
    return response


# Insert new product
def insert_new_product(connection, product):
    cursor = connection.cursor()

    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit) "
             "VALUES (%s, %s, %s);")

    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()

    last_row_id = cursor.lastrowid  # Store the ID of the newly inserted row
    cursor.close()  # Close cursor after use

    return last_row_id


# Delete a product
def delete_product(connection, product_id):
    cursor = connection.cursor()

    # Use parameterized query to avoid SQL injection
    query = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()

    rows_affected = cursor.rowcount  # Check how many rows were deleted
    cursor.close()  # Close cursor after use

    return rows_affected


# Main entry point
if __name__ == '__main__':
    connection = get_sql_connection()

    # Insert a new product
    new_product_id = insert_new_product(connection, {
        'product_name': 'cabbage',
        'uom_id': 1,
        'price_per_unit': 10
    })
    print(f"Inserted new product with ID: {new_product_id}")

    # Delete a product by ID
    product_id_to_delete = 9
    rows_deleted = delete_product(connection, product_id_to_delete)
    if rows_deleted > 0:
        print(f"Deleted product with ID: {product_id_to_delete}")
    else:
        print(f"No product found with ID: {product_id_to_delete}")

    # Get and print all products
    products = get_all_products(connection)
    for product in products:
        print(product)

    # Close the connection
    if connection.is_connected():
        connection.close()
        print("Connection closed.")
