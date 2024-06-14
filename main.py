#run: "uvicorn main:app" and append: "--reload"

from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()  #fastapi instance


#pydantic model/schema
#data is validated according to this schema
class Post(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property
    rating: Optional[int] = None  #fully optional field


my_posts = [
    {
        "title": "example title 1",  #my_posts[0].get("title")
        "content": "example content 1",  #my_posts[0]["content"]
        "id": 1
    },
    {
        "title": "example title 2",
        "content": "example content 2",
        "id": 2 
    }
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request

#it will only run the first path operation that matches
# @app.get("/")
# async def get_posts():
#     return {"data": "this is your posts"}

#the above get() and this post() are not the same thing
# @app.post("/")  #decorator
# async def root():  #function
#     return {"message2": "welcome to my api"}


@app.get("/posts")
def get_posts():
    # print(my_posts[0].get("title"))
    # print(my_posts[0]["content"])
    return {"data": my_posts}

#hits the first one irrespective of method name
# def root():  #function
#     return {"message": "welcome to my api"}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):  #extracting payload
#     print(payload)
#     return {"new_post": f"title {payload['title']} content {payload['content']}"}

@app.post("/posts")
def create_posts(new_post: Post):
    # print(new_post)  #new_post receives some JSON data from the Body
    # print(new_post.published)
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}  #sends this to the Post request


@app.get("/posts/{id}")  #this "id" field is a path parameter
def get_post(id: int):  #data type validation
    # print(id)  #path params are always str
    # return {"post_detail": f"here is post {id}"}
    post = find_post(id)
    return {"post_detail": post}

#timestamp: https://youtu.be/0sOvCWFmrtA?si=i4j4wDuCLpYgIvx4&t=6480