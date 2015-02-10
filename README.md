Instabot
========

Simple bot that use Instagrams API to like photos.
Creates an SQLite DB to record what pictures you have liked, therefore you

won't re-like pictures you have already liked.

Dependencies
===========
Instagrams API: https://github.com/Instagram/python-instagram


You can install it through pip


How To Use
==========
First, you must create an account with Instagram to get your token, and secret. 

Heres a post explaining how to do this: http://www.pygopar.com/playing-with-instagrams-api/

After all of that, you can run the program
~~~
from instabot import InstaBot

my_bot = InstaBot(token="Token_String", ip="Your_IP_ADDR", 
                  secret="Secret_Str", tag_list=["computerjoke"])
~~~