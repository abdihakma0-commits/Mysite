from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment

def blog_list(request):
    posts = Post.objects.filter(status='published')
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'comments': comments,
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