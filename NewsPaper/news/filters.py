from django_filters import FilterSet
 
from .models import Post
 
 
# создаём фильтр
class PostFilter(FilterSet):
    
    class Meta:
        model = Post
        fields = {
            'head_of_post': ['icontains'], 
            'post_date_created': ['gt'], 
            'post_author': ['in'], 
        }


