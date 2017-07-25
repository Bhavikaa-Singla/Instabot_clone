# if we are making a database driven app we need to make forms
from django import forms
from models import UserModel,PostModel,LikeModel,CommentModel



# forms are created using classes which consists of fields that are to be displayed in web pages
class SignUpForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields=['email','username','name','password']



# like user login form has fields username and password
class LoginForm(forms.ModelForm):
    class Meta:
         model = UserModel
         fields = ['username', 'password']



# like post form has fields image and caption
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image','caption']




class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']




class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']
