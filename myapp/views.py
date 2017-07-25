from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm,PostForm,LikeForm,CommentForm
from models import UserModel, SessionToken,PostModel,LikeModel,CommentModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime,timedelta
from django.utils import timezone
from djfight.settings import BASE_DIR

from paralleldots import set_api_key,get_api_key,sentiment
from imgurpython import ImgurClient


# sendgrid api is used to send automated emails to users
import sendgrid
# for this we import api key from api.py
# due to privacy concern i havent uploaded my sendgrid api key
from api import SENDGRID_API_KEY
from sendgrid.helpers.mail import*

import ctypes


YOUR_CLIENT_ID = '8059e06dee9e946'                                          #client id to access imgur api
YOUR_CLIENT_SECRET = '9ae7c8f156d74bf836c713baf7b6176f6c644893'


API_KEY = 'LrZefXNDQm7zNd4ANTGIAy3kDLNzrh8EiAA2sfU0LX4'                     #api key to access parallel dots api
set_api_key(API_KEY)


#Function declaration which shows sign up form to save the details for new user in the database on making required request
def signup_view(request):
    today = datetime.now()
    if request.method == "POST":
        form = SignUpForm(request.POST)                                                          #it will save the details of user in the database
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            if set('abcdefghijklmnopqrstuvwxyz').intersection(name) and set('abcdefghijklmnopqrstuvwxyz@_1234567890').intersection(username):
                if len(username) > 4 and len(password) > 5 and name.isspace()== False and username.isspace()== False:
                    user = UserModel(name=name, password=make_password(password), email=email,username=username)           # make_password is used to encrypt the password.
                    user.save()
                    # sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY))
                    # from_email = Email("bhavikasingla99@gamil.com")
                    # to_email = Email(form.cleaned_data['email'])
                    # subject = "Welcome to Instagram Clone!!"
                    # content = Content("text/plain", "Thank you for signing up  with Instagram Clone."
                    #                                 " Team , Instagram Clone.""  ")
                    # mail = Mail(from_email, subject, to_email, content)
                    # response = sg.client.mail.send.post(request_body=mail.get())
                    # print(response.status_code)
                    # print(response.body)
                    # print(response.headers)
                    ctypes.windll.user32.MessageBoxW(0, u"successfully signed up", u"success", 0)
                    return render(request, 'success.html')
                else:
                    ctypes.windll.user32.MessageBoxW(0, u"invalid enteries. please try again", u"Error", 0)
                    form = SignUpForm()                         # it will show the empty sign up form
            else:
                ctypes.windll.user32.MessageBoxW(0, u"invalid name/username", u"error", 0)
    else:
        form = SignUpForm()                                                                     #it will show the empty sign up form

    return render(request, 'index.html', { 'date_to_show':today, 'form': form})




def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):                             #it checks whether the entered password and hashed password saved in the database matches or not
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    ctypes.windll.user32.MessageBoxW(0, u"invalid username or password", u"Error", 0)
                    response_data['message'] = 'Incorrect Password! Please try again!'
            else:
                ctypes.windll.user32.MessageBoxW(0, u"invalid username or password", u"Error", 0)

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)




def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                ctypes.windll.user32.MessageBoxW(0, u"post successsfully created", u"SUCCESS", 0)

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')




def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None




def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')




def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                # like = LikeModel.objects.create(post_id=post_id, user=user)
                # sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY))
                # from_email = Email("apooravsharma1997@gmail.com")
                # to_email = Email(like.post.user.email)
                # subject = "Welcome to Instagram Clone!!"
                # content = Content("text/plain", "someone just liked your post. Go checkout!")
                # mail = Mail(from_email, subject, to_email, content)
                # response = sg.client.mail.send.post(request_body=mail.get())
                # print(response.status_code)
                # print(response.body)
                # print(response.headers)
            else:
                print existing_like.user.username
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')




def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            rev = sentiment(str(comment_text))
            review = rev["sentiment"]*100
            if review >= 60 and review <= 100:
                review = "Positive Comment!"
            elif review >= 40 and review < 60:
                review = "Neutral Comment!"
            elif review >= 0 and review < 40:
                review = "Negative Comment!"
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text, review=review)
            comment.save()
            # sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY))
            # from_email = Email("bhavikasingla99@gmail.com")
            # to_email = Email(comment.post.user.email)
            # subject = "Welcome to Instagram Clone!!"
            # content = Content("text/plain", "someone just commented on your post. Go check")
            # mail = Mail(from_email, subject, to_email, content)
            # response = sg.client.mail.send.post(request_body=mail.get())
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')




#for logging out the user from instagram clone
def logout_view(request):
    request.session.modified = True
    response = redirect('/login/')
    response.delete_cookie(key='session_token')
    return response




# def posts_of_particular_user(request,user_name):
#     posts=PostModel.objects.all().filter(user__username=user_name)
#     return render(request,'postsofuser.html',{'posts':posts,'user_name':user_name})
#     user = check_validation(request)
#     if user:
#         posts = PostModel.objects.all().filter(user__username=user_name)
#         return render(request, 'postsofuser.html', {'posts': posts, 'user_name': user_name})
#     else:
#         return redirect('/login/')