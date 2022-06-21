from unicodedata import category
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from requests import post
from .models import Post, Subscriber
from django.template.loader import render_to_string
from django.core.mail import send_mail



@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    
   
    subscribers = Subscriber.objects.filter()
    html_content = render_to_string('email_template.html', { 'head': instance.head_of_post, 'text':instance.article_text[:50], 'article_id':instance.id})
   
    category_post = list(instance.category.all())
    for sub in subscribers:
        if sub.category in category_post:
                msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {sub.name_sub.username}. Новая статья в твоём любимом разделе!',
                body=html_content,
                from_email='TestDjango1@yandex.ru',
                to=[sub.email,])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

        else:  
                continue

   
        
   