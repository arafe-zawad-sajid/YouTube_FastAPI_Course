#--- With Database (PostgreSQL) ---#

#run: "uvicorn app.main:app" and append: "--reload"

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()  #fastapi instance


#pydantic model/schema
#data is validated according to this schema
class Post(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property
    # rating: Optional[int] = None  #fully optional field
    

#--- Connecting to Database ---#
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='practice2', 
                                user='postgres', password='admin', cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print('DB conn was successful')
        break
    except Exception as error:
        print('DB conn failed')
        print('Error:', error)
        time.sleep(2)


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


#--- Get Posts---#
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()  #retrieve multiple posts
    # print(posts)
    return {"data": posts}


#--- Create Posts ---#
#sending status code with the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute(""" INSERT INTO posts (title, content, published)
    #                VALUES ({new_post.title}, {new_post.content}, {new_post.published}) """)
    #using f strings makes us vulnerable to SQL injection attack
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    #here we sanitize the input, more secured
    new_post = cursor.fetchone()
    conn.commit()  #save finalized staged changes
    return {"data": new_post}  #sends this to the Post request


#--- Get A Post ---#
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


#--- Delete A Post ---#
#sending status code with the decorator
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, 
                   (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#--- Update A Post ---# #fix it#
@app.put("/posts/{id}")
def update_post(id: int, post: Post):  #validate the data from frontend that is stored in post with our Post schema
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"data": updated_post}



#--- PostgreSQL ---#
# SELECT * FROM products;  #select all columns from products table

# SELECT name, id FROM products;  #select name, id columns from products table
#capitalization does not matter but SQL syntax keywords should be all caps

# SELECT id AS products_id, name AS product_name FROM products;  #renaming a col while viewing

# SELECT * FROM products WHERE id=10;  #info of a specific id

# SELECT * FROM products WHERE name='TV';  #varchar in single quotes, double quotes give error

# SELECT * FROM products WHERE price>80;
# SELECT * FROM products WHERE price>=80;

# SELECT * FROM products WHERE inventory!=0;
# SELECT * FROM products WHERE inventory<>0;

# SELECT * FROM products WHERE inventory>0 AND price>20;

# SELECT * FROM products WHERE price>100 OR price<20;

# SELECT * FROM products WHERE id=1 OR id=2 OR id=3;
# SELECT * FROM products WHERE id IN (1,2,3);  #products with id in the list

# SELECT * FROM products WHERE name LIKE 'TV%';  #products starting with TV
# SELECT * FROM products WHERE name LIKE '%en%';  #products that does not have 'en' in their name
# SELECT * FROM products WHERE name NOT LIKE '%en%';  #products that does not have 'en' in their name

# SELECT * FROM products ORDER BY price DESC;  #orders in ASC by default
# SELECT * FROM products ORDER BY inventory DESC, price ASC;  #sorts by inventory DESC then as tie breaker we sort by price ASC
# SELECT * FROM products ORDER BY created_at;  #oldest to newest, DESC to reverse

# SELECT * FROM products WHERE price>20 ORDER BY created_at DESC;

# SELECT * FROM products WHERE price>10 LIMIT 2;

# SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;  #offset 2 ignores/skips past the first 2

# INSERT INTO products (price, name, inventory) VALUES (10000, 'Car', 1000) RETURNING id;  #adds a product then returns all the cols
# INSERT INTO products (price, name, inventory) VALUES (10000, 'Car', 1000), (50, 'Laptop', 25), (60, 'Monitor', 4) RETURNING id;  #adds products then returns the id col

# DELETE FROM products WHERE id=10;
# DELETE FROM products WHERE id=11 RETURNING *;
# DELETE FROM products WHERE inventory=0;


# UPDATE products SET name='Flower', price=40 WHERE id=25;
# UPDATE products SET is_sale=true WHERE id=30 RETURNING *;
# UPDATE products SET is_sale=true WHERE id>15 RETURNING *;



#upto 4:28:35 - https://youtu.be/0sOvCWFmrtA?si=ERG6dw09WxqCSwHt&t=16116