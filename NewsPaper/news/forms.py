from pyexpat import model
from django.forms import ModelForm
from .models import Category, Post,Category,Subscriber
from django import forms
 
# Создаём модельную форму
class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['head_of_post', 'article_text', 'post_author', 'category', 'post_type']


class SubscriberForm(forms.Form):
    email = forms.EmailField()
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), initial='detective')
    class Meta:
        model = Subscriber
        fields = ['email',]