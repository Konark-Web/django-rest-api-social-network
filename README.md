Object of this task is to create a simple REST API use DRF.


## Basic models:
- User
- Post (always made by a user)

## Basic Features:
- user signup
- user login
- post creation
- post like
- post unlike
- analytics about how many likes was made. Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated by day. 
- user activity an endpoint which will show when user was login last time and when he mades a last request to the service.


## Requirements:
- Implement token authentication (JWT is prefered)

### Endpoints:
- /api/posts (GET) - get all posts
- /api/posts/<id> (GET) - get single post by id
- /api/posts/<id>/like (POST) - like or unlike post by id
- /api/post-create/ (POST) - create new post
- /api/create-user/ (POST) - registration endpoint
- /api/authenticate/ (POST) - authentication for get token



