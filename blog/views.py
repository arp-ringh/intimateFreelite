from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import View
#from .models import Post


# Create your views here.
class BaseView(View):
    views = {}


class HomeView(BaseView):
    def get(self, request):
        self.views['posts'] = Post.published.all()
        self.views['categories'] = Category.objects.all()
        self.views['subcategories'] = Subcategory.objects.all()
        return render(request,'index.html', self.views)


#def blog_list(request):
#    #posts = Post.objects.filter(status="published")
#    posts = Post.published.all()
#    return render(request, 'index.html', {'posts':posts})


#def blog_single(request, post):
#    post=get_object_or_404(Post, slug=post,status='published')
#    return render(request, 'single.html', {'post':post})


#def blogSingle(BaseView, post):
#    def get(self,request):
#        self.views['post'] = get_object_or_404(Post, slug=post, status='published')
#        return render(request, 'single.html', self.views)

class blogSingle(BaseView):
    def get(self,request,post):
        self.views['post'] = get_object_or_404(Post, slug=post, status='published')
        return render(request, 'single.html', self.views)

class SubCategoryView(BaseView):
    def get(self,request,slug):
        subcat = Subcategory.objects.get(slug = slug).id
        self.views['subcat_posts'] = Post.objects.filter(subcategory_id  = subcat)
        self.views['subcat_title'] = Subcategory.objects.get(slug = slug).name

        return render(request,'subcategory.html',self.views)
