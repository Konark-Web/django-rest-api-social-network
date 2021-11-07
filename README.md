Object of this task is to create a simple REST API use DRF.
The project also uses Celery+Flower and Redis to send messages.


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

## Endpoints:
- /api/posts (GET) - get all posts
- /api/posts/<post-id> (GET) - get single post by id
- /api/posts/<post-id>/like (POST) - like or unlike post by id
- /api/post-create/ (POST) - create new post
- /api/create-user/ (POST) - registration endpoint
- /api/authenticate/ (POST) - authentication for get token by email and password
- /api/analytics/?date_from=2021-02-02&date_to=2021-11-10 (GET) - analytics about how many likes was made. API return 
analytics aggregated by day. date_from is required parameter.

### Response examples:
https://gist.github.com/Konark-Web/e9961fea2709b0b58a31b6d89358f0c2




