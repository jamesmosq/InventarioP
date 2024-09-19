# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'product_database'
}

# Table configuration
TABLE_NAME = "products"
COLUMNS = [
    ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
    ("name", "VARCHAR(255) NOT NULL"),
    ("brand", "VARCHAR(255) NOT NULL"),
    ("reference", "VARCHAR(255) NOT NULL"),
    ("price", "DECIMAL(10, 2) NOT NULL"),
    ("quantity", "INT NOT NULL")
]