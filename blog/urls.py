#urls.py of blog app
from django.urls import path
#from .views import *
from . import views
from .views import *

app_name = "blog"


urlpatterns = [
    path('',HomeView.as_view(), name = 'blog'),
    #path('',views.blog_list,name='blog_list'),
    #path('<slug:post>/',views.blog_single,name="blog_single"),
    #path('<slug:post>/',blogSingle.as_view(),name="single"),
    path('subcategory/<slug>',SubCategoryView.as_view(),name="subcategory"),
    path('<slug:post>/',views.blogSingle,name="single"),
    path('comment/reply/', views.reply_page, name="reply"), 
    path('tag/<slug:tag_slug>/',HomeView.as_view(), name='post_tag'),
    path('search', SearchView.as_view(), name='search'),
    path('contact', views.contact, name='contact')



        ]
