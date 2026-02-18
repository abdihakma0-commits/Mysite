from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category, Comment

def blog_list(request):
    posts = Post.objects.filter(status='published')
    categories = Category.objects.all()
    
    # Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    context = {
        'posts': posts,
        'categories': categories,
        'query': query,
    }
    return render(request, 'blog/list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment views
    post.views += 1
    post.save()
    
    # Get comments
    comments = post.comments.filter(is_approved=True)
    
    # Handle comment submission
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        if request.user.is_authenticated:
            comment = Comment(
                post=post,
                user=request.user,
                name=request.user.username,
                email=request.user.email,
                content=content
            )
        else:
            comment = Comment(
                post=post,
                name=name,
                email=email,
                content=content
            )
        
        comment.save()
        messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        return redirect('blog_detail', slug=slug)
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    }
    return render(request, 'blog/detail.html', context)

def blog_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)