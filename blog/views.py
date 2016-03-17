from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 5) #5 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         #if page is not an integer deliver first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         #if page is out of range deliver the last one
#         posts = paginator.page(paginator.num_pages)
#     context = {
#         'page' : page,
#         'posts' : posts,
#     }
#     return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    #list of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        #a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment but don't save to db
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post = post
            #save comment to db
            new_comment.save()
    else:
        comment_form = CommentForm
    context = {
        'post' : post,
        'comments' : comments,
        'comment_form' : comment_form,
    }
    return render(request, 'blog/post/detail.html', context)

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments']
            )
            send_mail(subject, message, 'admin@gajownik.com', cd['to'])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post' : post,
        'form' : form,
        'sent' : sent,
    }
    return render(request, 'blog/post/share.html', context)