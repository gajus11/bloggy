from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 5) #5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver the last one
        posts = paginator.page(paginator.num_pages)
    context = {
        'page' : page,
        'posts' : posts,
    }
    return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post' : post})