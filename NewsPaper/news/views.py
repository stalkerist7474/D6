from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Subscriber

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .filters import PostFilter
from .forms import NewsForm, SubscriberForm
 
class NewsList(ListView):
    model = Post  
    template_name = 'news.html'  
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='NW').order_by('-id')  
    paginate_by = 10

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
        

        context['head_of_post'] = Post.objects.all()
        context['article_text'] = Post.objects.all()
        context['post_author'] = Post.objects.all()
        context['post_type'] = Post.objects.all()
        context['category'] = Post.objects.all()


        context['form'] = NewsForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = NewsForm(request.POST) 
 
        if form.is_valid(): 
            form.save()
 
        return super().get(request, *args, **kwargs)
    
    

class NewsListForSearck(ListView):
    model = Post  
    template_name = 'search.html'  
    context_object_name = 'searchNews'
    queryset = Post.objects.filter(post_type='NW').order_by('-id')  
    #paginate_by = 10

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
        return context





class NewsDetail(DetailView):
    model = Post 
    template_name = 'newsDetail.html' 
    context_object_name = 'newsDetail' 
    queryset = Post.objects.filter(post_type='NW')

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create_news.html'
    form_class = NewsForm
    permission_required = ('news.add_post',
                           'news.view_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

# дженерик для редактирования объекта
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = NewsForm
    permission_required = ('news.change_post',
                           'news.view_post')
 
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
 
# дженерик для удаления товара
class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',
                           'news.view_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

@login_required
@csrf_exempt
def subsribe_me(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        print(form)
        email_entered = form.cleaned_data['email']
        category_chosen = form.cleaned_data['category']
        print(category_chosen)
        b = str(category_chosen[0])
        if not Subscriber.objects.filter(email=email_entered).exists() and b == 'fiction':
            Subscriber.objects.create(email=email_entered)
        return HttpResponseRedirect('/news/')         
    else:
        return render(request,'subscribe.html', {'form': SubscriberForm(initial={'email':request.user.email})})