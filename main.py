#run: "uvicorn main:app" 
#append: "--reload"

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()  #fastapi instance

# pydantic model/schema
class Post(BaseModel):
    title: str
    content: str


# path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": "your posts"}

@app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content {payload['content']}"}
def create_posts(new_post: Post):
    return {"data": "new post"}
