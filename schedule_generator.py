
import os
2
import requests
3
def send_simple_message():
4
    return requests.post(
5
      "https://api.mailgun.net/v3/sandbox49f1250bdeb647d1a93c4e0226d09a79.mailgun.org/messages",
6
      auth=("api", 'd9338c9d147f9a1fd6d9fe18baa20c99-d2d7ea9a-f158948e'),
7
      data={"from": "Mailgun Sandbox <postmaster@sandbox49f1250bdeb647d1a93c4e0226d09a79.mailgun.org>",
8
      "to": "Matheus Cruz <matheuscz3110@gmail.com>",
9
        "subject": "Hello Matheus Cruz",
10
        "text": "Congratulations Matheus Cruz, you just sent an email with Mailgun! You are truly awesome!"})