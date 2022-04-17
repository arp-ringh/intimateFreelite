from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CommentForm
from django.views.generic import View
from django.db.models import Count
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

#class blogSingle(BaseView):
#    def get(self,request,post):
#        self.views['post'] = get_object_or_404(Post, slug=post, status='published')
#        # List of active comments for this post
#        self.views['comments'] = self.views['post'].comments.filter(active=True)
#        self.views['comment_form'] = CommentForm()
#        return render(request, 'single.html', self.views)
#

# blogSingle named to _blogSingle as its not working to CBD
class _blogSingle(BaseView):
    def get(self,request,post):
        self.views['post'] = get_object_or_404(Post, slug=post, status='published')
        # List of active comments for this post
        self.views['comments'] = self.views['post'].comments.filter(active=True)
        #self.views['comment_form'] = CommentForm()
        
        self.views['new_comment'] = None

        if self.request.method == 'POST':
            # A comment was posted
            self.views['comment_form'] = CommentForm(data=request.POST)
            if self.views['comment_form'].is_valid():
                # Create Comment object but don't save to database yet
                self.views['new_comment'] = self.views['comment_form'].save(commit = False)
                # Assign the current post to the comment
                self.views['new_comment'].self.views['post'] = self.views['post']
                # Save the comment post to the comment
                self.views['new_comment'].save()
                # redirect to same page and focus on that comment
                return redirect(self.views['post'].get_absolute_url()+'#'+str(self.views['new_comment'].id))
        else:
            self.views['comment_form'] = CommentForm()

        return render(request, 'single.html', self.views)



def blogSingle(request,post):
    post = get_object_or_404(Post,slug=post,status='published')

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()


    return render(request, 'single.html',{'post':post,'comments': comments,'comment_form':comment_form})


# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')   # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url') # from hidden input

            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")







class SubCategoryView(BaseView):
    def get(self,request,slug):
        subcat = Subcategory.objects.get(slug = slug).id
        self.views['subcat_posts'] = Post.objects.filter(subcategory_id  = subcat)
        self.views['subcat_title'] = Subcategory.objects.get(slug = slug).name

        return render(request,'subcategory.html',self.views)



