#run: "uvicorn v10.app.main:app" and append: "--reload" for auto reload

#--- Voting System ---#
#A user should be able to like a post once
#Anytime we retrieve the posts from our db/API we should also fetch the total no. of likes     
#We store the votes in another db table
#Every "post_id" and "user_id" pairs should be unique, we use composite keys here  
#It is just a primary key that spans multiple cols (instead of just 1) and ensures that accross those cols we have uniqne combinations
#Since a primary key must be unique, so we just make sure both the cols are part of the primary key 
#A composite primary key doesn't care if there are duplicates in any col, rather the col pairs
#In pgadmin, we just create "votes" table and set both "post_id" and "user_id" cols as primary keys
#We should setup two foreign keys for the two relationships, 
#one between posts and votes, another between users and votes 
#we make sure if a post or a user is deleted, it should cascade delete the related vote entries
#the foreign keys make sure we can't make an entry with non-existent user_id or post_id
#we need to setup the vote route in "routers\vote.py"
#When we retrieve posts we want FastAPI to send the no. of votes as a property/field,
#we want to see the no. of likes a post has, we should automatically send that info instead of making another query to our backend
#for that we use the JOIN keyword in SQL
#      

#--- SQL JOIN ---#
#Now that we have more than one table and relationships, we want to get infos from two table at once
#We can JOIN two tables together with a single query, that's more efficient than multiple queries 
#link: https://www.postgresqltutorial.com/ 

# SELECT * FROM posts LEFT JOIN users ON posts.owner_id = users.id 
#The left join starts selecting data from the left table (posts)
#It compares vals from posts.owner_id col with vals from users.id col in the users table
#If these vals are equal, it creates a new row that contains cols of both tables and adds this new row to the result set
#If the vals are not equal, it still creates a new row that contains cols from both tables and adds it to the result set, 
#but it fills the cols of the right table (users) with null 
#Lists out each post and it's corresponding owner, 1 post must have 1 owner
#The left table (posts) has more precedence here, if a user made no posts then it doesn't list out the user info
#If there was a post without an owner_id the user info would be shown as null,
#since our posts table must have an owner_id so we won't run into such a situation 

# SELECT title, content, email FROM posts LEFT JOIN users ON users.id=posts.owner_id

# SELECT id, content, email FROM posts LEFT JOIN users ON users.id=posts.owner_id
#It throws an error because both tables have an id col, so we have to be specific
#The cols content and email are exclusive to their respective tables, which is fine
#To resolve the error/confusion we just append the table name
# SELECT posts.id, users.email FROM posts LEFT JOIN users ON users.id=posts.owner_id

# SELECT posts.*, email FROM posts LEFT JOIN users ON users.id=posts.owner_id  
#Grabs all the cols from the posts table and email col from users table

# SELECT * FROM posts RIGHT JOIN users ON posts.owner_id = users.id
#RIGHT JOIN is reverse of LEFT JOIN, direction is opposite
#Lists out each user and their corresponding posts, 1 user can make 0-n posts
#The right table (users) has more precedence here, if a user made no posts still it lists out the user info but the post infos are null

#In a RIGHT JOIN we'll get instances where something exists in the right table (users) but doesn't exist in the left table (posts)
#In a LEFT JOIN we'll get instances where something exists in the left table (posts) but doesn't exist in the right table (users)

#We want to get the no. of posts by each user 

# SELECT users.id, COUNT(*) FROM posts LEFT JOIN users ON posts.owner_id=users.id GROUP BY users.id
#We'll GROUP the entries from our JOIN based on users.id, once we group them we can count all of the entries per user
#One user made no posts so we don't see it

# SELECT users.id, COUNT(*) FROM posts RIGHT JOIN users ON posts.owner_id=users.id GROUP BY users.id
#It seems to have worked but the count is 1 for the user with 0 posts, it counts the null entries

#Instead of COUNT(*) we should pass in a col (any posts col) that we wanna count, to avoid counting null entries  
#If a user didn't make a post then posts.id would be null
# SELECT users.id, COUNT(posts.id) FROM posts RIGHT JOIN users ON posts.owner_id=users.id GROUP BY users.id
#This works perfectly

# SELECT users.id, users.email, COUNT(posts.id) AS user_post_count FROM posts RIGHT JOIN users ON posts.owner_id=users.id GROUP BY users.id
#just renaming the col

#Now we work with our posts and votes tables, we'll JOIN them
# SELECT * FROM posts LEFT JOIN votes ON posts.id = votes.post_id
#We have posts that are being repeated because we print a row everytime the posts.id matches votes.post_id
#We have multiple votes for a post, that's why the post entries are being repeated 

# SELECT * FROM posts RIGHT JOIN votes ON posts.id = votes.post_id
#It's gonna do the exact opposite
#Some posts will be shown multiple times since multiple users voted on them
#It's going to show us all of the votes and their corresponding posts

#we want to count the total no. of votes for each posts
# SELECT posts.id, COUNT(*) FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id
#Like before, it's counting the null entries as 1, we don't want that 

# SELECT posts.id, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id
#We get the post_id and no. of votes

# SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id
#This is the exact query that we need, we have the post info and the no. of votes

#To get the no. of votes for an individual post we just add the WHERE condition
# SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id=11 GROUP BY posts.id
#    


from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#setting up stuff
models.Base.metadata.create_all(bind=engine)  #creates db tables
app = FastAPI()  #fastapi instance

app.include_router(post.router)  #importing the router obj from post.py
app.include_router(user.router)  #the request will go into user.py and look for the route
                                 #if it finds a match it will respond like it normally does
app.include_router(auth.router)
app.include_router(vote.router)

#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


