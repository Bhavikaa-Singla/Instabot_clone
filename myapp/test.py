from paralleldots import set_api_key,get_api_key
from paralleldots import hit_count, specific_hit_count



API_KEY = 'LrZefXNDQm7zNd4ANTGIAy3kDLNzrh8EiAA2sfU0LX4'



set_api_key(API_KEY)
print get_api_key()

print hit_count()
print specific_hit_count( "multilang_sentiment" )
