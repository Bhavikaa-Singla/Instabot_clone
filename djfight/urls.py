# we create urls in django in url.py file
# for this we have to import urls from django.conf.url
from django.conf.urls import url
#from views we import pages which we are giving to url
from myapp.views import signup_view,login_view,feed_view,post_view,like_view,comment_view,logout_view

# there are the patterns which we use to create url for a particular page
# r is the regular expression

urlpatterns = [

    # url(r'^login/feed/(?P<user_name>.+)/$', posts_of_particular_user),
    url('logout/', logout_view, name='logout'),
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url('login/', login_view),
    url('', signup_view),

]