from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    full_name = models.CharField(max_length = 255)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    raiting = models.IntegerField(default = 1)

    def update_raiting(self):
        post_raiting = self.post_set.all().aggregate(sumraiting = Sum('post_raiting'))
        authors_post_raiting = 0
        authors_post_raiting = authors_post_raiting + post_raiting.get('sumraiting')

        comment_raiting = self.user.comment_set.all().aggregate(sumraiting1 = Sum('comment_raiting'))
        authors_comment_raiting = 0
        authors_comment_raiting = authors_comment_raiting + comment_raiting.get('sumraiting1')
   
        authors_post_comment_raiting = 0
        j=[]
        m=0
        for i in self.post_set.all():
                j.append(i)
                comment_raiting3 = self.user.comment_set.filter(post=j[m]).aggregate(sumraiting1 = Sum('comment_raiting'))
                authors_post_comment_raiting += comment_raiting3.get('sumraiting1')
                m=m+1 
            
        self.raiting = 3 * authors_post_raiting + authors_post_comment_raiting + authors_comment_raiting
        self.save()
    def __str__(self):
        return f'{self.full_name.title()}'


class Category(models.Model):
    category_name = models.CharField(max_length = 255, unique = True)
    def __str__(self):
        return f'{self.category_name.title()}'


class Post(models.Model):
    post = 'PO'
    news = 'NW'
    POSITIONS=[
    (post,'post'), 
    (news,'news'),]
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= POSITIONS)
    post_date_created = models.DateField(auto_now_add = True)
    post_detailed_time_created = models.TimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    head_of_post = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default = 1)

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def preview(self):
        review = self.article_text[:124]+'...'
        return review

    def __str__(self):
        return f'{self.head_of_post.title()}'

    def get_absolute_url(self): 
        return f'/news/{self.id}' 
    
    

    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'{self.post} category post: {self.category}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User,on_delete = models.CASCADE)
    comment_text = models.TextField()
    comment_date_created = models.DateField(auto_now_add = True)
    comment_raiting = models.IntegerField(default = 1) 
    
    def like(self):
        self.comment_raiting +=1
        self.save()
    
    def dislike(self):
        self.comment_raiting -=1
        self.save()

class Subscriber(models.Model):
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
    name_sub = models.OneToOneField(User,on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.email