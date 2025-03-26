from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User

from blog.views import index, create_post, post_detail, login_view, logout_view, signup, signup_view, posts, category_posts, delete_post, like_post, post_edit, category_search, category_posts, delete_comment, add_comment

urlpatterns = [
    path('', index, name="index"),
    path('create/', create_post, name='create_post'),
    path('posts/', posts, name='posts'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('category/<int:category_id>/', category_posts, name='category_posts'),
    path('post/<int:post_id>/delete/', delete_post, name='post_delete'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('category_search/', category_search, name='category_search'),
    path('category/<int:category_id>/', category_posts, name='category_posts'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),  # ✅ Fix: Define the delete_comment URL
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),

]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)