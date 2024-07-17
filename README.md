# simple-accesstoken-manager
A simple but functional access token manager for webapps and web systems

# How to calculate the personal token for /validate/ endpoint
To calculate this parameter we need the username and password as a SHA-256 string.
First step is to get last 32 characters of the username hash.
Then, get the first 32 characters of the password hash.
Finally, the personal token can be obtained as a SHA-256 hash of this new string

PERONAL TOKEN = SHA-256(first 32 chars from password HASH + last 32 chars of username HASH)

# TODOS
1. Endpoint to register new users
1. Routines to authenticate admin user
1. Link to frontend project (https://github.com/artnicbr/panel-token-manager)