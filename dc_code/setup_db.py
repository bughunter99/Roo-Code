import sqlite3

conn = sqlite3.connect('sample.db')
c = conn.cursor()

# users 테이블에 데이터 추가
c.execute("INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@example.com', 28)")
c.execute("INSERT INTO users (name, email, age) VALUES ('Bob', 'bob@example.com', 32)")
c.execute("INSERT INTO users (name, email, age) VALUES ('Charlie', 'charlie@example.com', 25)")

# products 테이블 생성
c.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    price REAL, 
    category TEXT
)''')

c.execute("INSERT INTO products (name, price, category) VALUES ('Laptop', 1200.00, 'Electronics')")
c.execute("INSERT INTO products (name, price, category) VALUES ('Mouse', 29.99, 'Electronics')")
c.execute("INSERT INTO products (name, price, category) VALUES ('Keyboard', 79.99, 'Electronics')")

conn.commit()
conn.close()
print('✓ sample.db 생성 및 데이터 추가 완료')
