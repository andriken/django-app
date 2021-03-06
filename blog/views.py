from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.decorators.csrf import csrf_exempt



def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    query = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if 'search' in request.GET:
        if len(request.GET.get('search')) > 0:
            query = request.GET.get('search')
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            object_list = Post.published.annotate(search=search_vector,
                                                    rank=SearchRank(search_vector, search_query)
                                                    ).filter(search=search_query).order_by('-rank')


    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    print(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page Is not an Integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of ranger deliver last page of the result
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html', {'page': page,
                                                'posts': posts,
                                                'tag': tag,
                                                'searchquery': query})


"""
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'blog/post/list.html'
"""

@csrf_exempt
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    downloadlink = None
    if request.method == 'POST':
        # A comment was posted
        downloadlink = request.POST.get("downloadlink")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similiar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')
    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form,
                                                    'similar_posts':similar_posts,
                                                     'downloadlink': downloadlink})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ...send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends your read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'nfsrivalsuploaded@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent':sent})


def privacy_disclaimer(request):
    return render(request, 'blog/privacy-policy.html')


def gdpr_policy(request):
    return render(request, 'blog/gdpr-policy.html')