from paralleldots import set_api_key,get_api_key
from paralleldots import hit_count, specific_hit_count,sentiment



API_KEY = 'LrZefXNDQm7zNd4ANTGIAy3kDLNzrh8EiAA2sfU0LX4'



set_api_key(API_KEY)
print get_api_key()

t = sentiment("Come on! lets play together")
print t["sentiment"]*100
print sentiment("hey there!!Whats up??")
print sentiment("not so good,not so bad")
# print hit_count()
# print specific_hit_count( "multilang_sentiment" )
