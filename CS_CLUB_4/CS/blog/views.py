from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.utils.text import slugify
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import Post
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
from .models import Post, Comment, Category
from django.contrib.auth.forms import UserCreationForm


def index(request):
    latest_posts = Post.objects.order_by("-created_at")[:6]  # Get newest 6 posts
    return render(request, "blog/index.html", {"posts": latest_posts})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_category_name = form.cleaned_data.get("new_category")
            category = form.cleaned_data.get("category")

            # If the user entered a new category, create or get it
            if new_category_name:
                category, created = Category.objects.get_or_create(
                    name=new_category_name
                )

            # Save post with the selected or newly created category
            post = form.save(commit=False)
            post.category = category
            post.author = request.user
            post.save()
            return redirect("post_detail", post.id)
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})

def category_search(request):
    query = request.GET.get("q", "").strip()  # Get search query and remove extra spaces

    if not query:
        # Option 1: Show message and reload the same page
        messages.error(request, "Please enter a search term.")
        return render(request, "blog/category_search.html", {"query": "", "categories": None, "posts": []})

        # Option 2 (alternative): Redirect to another page
        # return redirect("home")  # Replace with your desired URL name

    # Search logic
    categories = Category.objects.filter(name__icontains=query)
    posts = Post.objects.filter(category__in=categories) if categories.exists() else []

    return render(
        request,
        "blog/category_search.html",
        {"query": query, "categories": categories, "posts": posts},
    )

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(
        request, "blog/category_posts.html", {"category": category, "posts": posts}
    )


def posts(request):
    category_id = request.GET.get("category")
    posts = Post.objects.all()

    if category_id:
        posts = posts.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(
        request, "blog/posts.html", {"posts": posts, "categories": categories}
    )


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(
        request, "blog/category_posts.html", {"posts": posts, "category": category}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Fetch comments
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[
        :3
    ]  # Fetch up to 3 related posts

    # Handle like/unlike functionality
    if request.method == "POST" and "like_post" in request.POST:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)  # Unlike if already liked
        else:
            post.likes.add(request.user)  # Like if not liked yet
        return redirect("post_detail", post_id=post.id)

    # Handle comment functionality
    if request.method == "POST" and "comment" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    # Determine if the current user has liked the post
    liked = (
        post.likes.filter(id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "related_posts": related_posts,
            "liked": liked,  # Pass the liked status to the template
        },
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")  # Redirect to home page
        else:
            return render(
                request, "blog/login.html", {"error": "Invalid username or password."}
            )

    return render(request, "blog/login.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect("index")  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()
    return render(request, "blog/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# def signup_view(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Account created successfully! 🎉")
#             return redirect("index")
#         else:
#             messages.error(request, "Error creating account. Please check the form.")
#     else:
#         form = SignupForm()

#     return render(request, "blog/signup.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only allow the post author to delete it
    if request.user == post.author:
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("posts")  # Redirect to all posts

    messages.error(request, "You are not authorized to delete this post.")
    return redirect("post_detail", post_id)  # Prevent unauthorized access


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike if already liked
        liked = False
    else:
        post.likes.add(request.user)  # Like if not liked yet
        liked = True

    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the author can edit
    if request.user != post.author:
        return redirect("post_detail", post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_edit.html", {"form": form, "post": post})


def user_login(request):
    if request.user.is_authenticated:  # Skip login if already signed in
        return redirect("index")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirect to home page after login
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect(
                "post_detail", post_id=post.id
            )  # Redirect back to the post detail page
    return HttpResponse("Invalid request", status=400)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post

    # Check if the logged-in user is the author of the post
    if request.user == post.author:
        # Delete the comment
        comment.delete()
        return redirect("post_detail", post_id=post.id)
    else:
        # If the user is not the author, return a forbidden response
        return HttpResponseForbidden("You are not authorized to delete this comment.")
