from db import get_connection

def create_tables():    
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            email VARCHAR(150) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date TIMESTAMPTZ DEFAULT NOW(),
            total_amount DECIMAL(10, 2) NOT NULL,
            order_status VARCHAR(50) NOT NULL,
            shipping_address TEXT NOT NULL,
            CONSTRAINT fk_user
                FOREIGN KEY (user_id) 
                REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id VARCHAR(100) NOT NULL, -- Soft link referencing MongoDB product _id/sku
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            CONSTRAINT fk_order
                FOREIGN KEY (order_id) 
                REFERENCES orders (order_id)
                ON DELETE CASCADE
        );
        """
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
        conn.commit()