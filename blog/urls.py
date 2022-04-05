#urls.py of blog app
from django.urls import path
#from .views import *
#from . import views
from .views import *

app_name = "blog"


urlpatterns = [
    path('',HomeView.as_view(), name = 'blog'),
    #path('',views.blog_list,name='blog_list'),
    #path('<slug:post>/',views.blog_single,name="blog_single"),
    path('<slug:post>/',blogSingle.as_view(),name="single"),






        ]
