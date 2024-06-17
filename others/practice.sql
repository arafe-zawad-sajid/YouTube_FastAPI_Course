SELECT * FROM products;

SELECT name FROM products;
SELECT name, id FROM products;

SELECT id AS products_id FROM products;
SELECT id AS products_id, name AS product_name FROM products;

SELECT * FROM products WHERE id=10;
SELECT * FROM products WHERE inventory=0;
SELECT * FROM products WHERE name='TV';

SELECT * FROM products WHERE price>80;
SELECT * FROM products WHERE price>=80;

SELECT * FROM products WHERE inventory!=0;
SELECT * FROM products WHERE inventory<>0;

SELECT * FROM products WHERE inventory>0 AND price>20;

SELECT * FROM products WHERE price>100 OR price<20;

SELECT * FROM products WHERE id=1 OR id=2 OR id=3;
SELECT * FROM products WHERE id IN (1,2,3);

SELECT * FROM products WHERE name LIKE 'TV%';
SELECT * FROM products WHERE name LIKE '%en%';
SELECT * FROM products WHERE name NOT LIKE '%en%';

SELECT * FROM products ORDER BY price DESC;
SELECT * FROM products ORDER BY inventory DESC, price ASC;
SELECT * FROM products ORDER BY created_at;

SELECT * FROM products WHERE price>20 ORDER BY created_at DESC;

SELECT * FROM products WHERE price>10 LIMIT 2;

SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;

INSERT INTO products (name, price, inventory) VALUES ('Tortilla', 4, 1000)











