#run: "uvicorn main:app" and append: "--reload"

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()  #fastapi instance

#pydantic model/schema
class Post(BaseModel):
    title: str  #var name and data type same as body
    content: str  #var name and data type same as body


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
    return {"data": "this is your posts"}

#hits the first one irrespective of method name
# def root():  #function
#     return {"message": "welcome to my api"}


@app.post("/createposts")
# def create_posts(payload: dict = Body(...)):  #extracting payload
#     print(payload)
#     return {"new_post": f"title {payload['title']} content {payload['content']}"}
def create_posts(new_post: Post):
    print(new_post)  #new_post receives some JSON data from the Body
    return {"data": "new post"}  #sends this to the Post request




#timestamp: https://youtu.be/0sOvCWFmrtA?si=ih3pZheDmErUAD9k&t=4393