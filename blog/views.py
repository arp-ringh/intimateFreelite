from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CommentForm
from django.views.generic import View
from django.db.models import Count, Q
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.contrib.auth.models import User as coreUser
# User imported as coreUser as username of tweepy conflicted with django User
from django.contrib import messages
import tweepy

# Create your views here.
class BaseView(View):
    views = {}


class HomeView(BaseView):
    def get(self, request, tag_slug=None):
        self.views['posts'] = Post.published.all()
        self.views['categories'] = Category.objects.all()
        self.views['subcategories'] = Subcategory.objects.all()
        self.views['comment'] = Comment.objects.all()
        self.views['popular_posts']= Post.published.filter(section = 'popular')
        self.views['home_posts'] = Post.published.filter(section = 'home')
        self.views['recent_posts'] = Post.published.filter(section = 'recent')
        #Retrieve posts according totags
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            paginator = Paginator(Post.published.filter(tags__in=[tag]),5) 
 
        else:
            paginator = Paginator(Post.published.all(),5) 
        page = request.GET.get('page')
        self.views['pages'] = paginator.get_page(page)

        # tweepy
        users = User.objects.get(screen_name='ArpRingh')
        self.views['tweets'] = Tweet.public_tweet_objects.filter(user=users)
        # user was changed to users as there was conflict bulit in user
        # with django authenctication while user was passed as context

        auth = tweepy.OAuth1UserHandler('nmIQy6tzAsv3frSvFrB2O4u79',
                                        'sU6HIeOzDAtW95gIdtBsaXF7jIxy4BLSk0iKfiSlMDogISrHI6',
                                        '1518565332369436672-495NUdkYYCb7M798spd7AYyt7eDWrL',
                                        'iX41RQes5CWmIjZgOB2eH1XHCZ1FmTDdB0BOeOdhzJFIj'
                                        )
        api = tweepy.API(auth)

        self.views['users'] = api.get_user(screen_name='ArpRingh')
        self.views['public_tweets'] = api.home_timeline()
        # tweepy


        return render(request,'index.html', self.views)



def blogSingle(request,post):
    post = get_object_or_404(Post,slug=post,status='published')
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    popular_posts = Post.published.filter(section = 'popular')
    home_posts = Post.published.filter(section = 'home')
    recent_posts = Post.published.filter(section = 'recent')
    
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


    # Similar Posts
    tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.published.filter(tags__in=tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]
    

    # tweepy
    users = User.objects.get(screen_name='ArpRingh')
    # above User is not django User perhaps belonging to tweepy
    # also django User needed to be imported as coreUser due to this reason
    tweets = Tweet.public_tweet_objects.filter(user=users)
    # user was changed to users as there was conflict bulit in user
    # with django authenctication while user was passed as context

    auth = tweepy.OAuth1UserHandler('nmIQy6tzAsv3frSvFrB2O4u79',
                                    'sU6HIeOzDAtW95gIdtBsaXF7jIxy4BLSk0iKfiSlMDogISrHI6',
                                    '1518565332369436672-495NUdkYYCb7M798spd7AYyt7eDWrL',
                                    'iX41RQes5CWmIjZgOB2eH1XHCZ1FmTDdB0BOeOdhzJFIj'
                                    )
    api = tweepy.API(auth)

    users = api.get_user(screen_name='ArpRingh')
    public_tweets= api.home_timeline()
    # tweepy

    context = {
            'post':post,
            'comments': comments,
            'comment_form':comment_form,
            'related_posts':related_posts,
            'categories':categories,
            'subcategories':subcategories,
            'popular_posts':popular_posts,
            'home_posts':home_posts,
            'recent_posts':recent_posts,
            'users':users,
            'public_tweets':public_tweets,
            }

    return render(request, 'single.html',context)


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


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        data = Contact.objects.create(name=name, email=email, subject=subject, message=message)
        data.save()

    try:
        email = EmailMessage('Hello', 'Thanks! For Messaging Us, We will get back to you soon.', 'arpringh@gmail.com', [email])
        email.send()
    except:
        pass
    else:
        messages.success(request,'Email has sent !')
        return redirect('blog:contact')


    return render(request, 'contact.html')



class SearchView(BaseView):
    def get(self,request):
        if request.method == 'GET':
            query = request.GET['query']
            self.views['search_name'] = query
            lookups = Q(title__icontains = query) | Q(excerpt__icontains = query) | Q(body__icontains = query)

            self.views['search_posts'] = Post.objects.filter(lookups)
        return render(request,'search.html',self.views)



from ditto.twitter.models import User, Tweet
# just for testing tweepy package
class ditto(BaseView):
    def get(self,request):
        users = User.objects.get(screen_name='ArpRingh')
        self.views['tweets'] = Tweet.public_tweet_objects.filter(user=users)
        

        auth = tweepy.OAuth1UserHandler('nmIQy6tzAsv3frSvFrB2O4u79',
                                        'sU6HIeOzDAtW95gIdtBsaXF7jIxy4BLSk0iKfiSlMDogISrHI6',
                                        '1518565332369436672-495NUdkYYCb7M798spd7AYyt7eDWrL',
                                        'iX41RQes5CWmIjZgOB2eH1XHCZ1FmTDdB0BOeOdhzJFIj'
                                        )
        api = tweepy.API(auth)

        self.views['users'] = api.get_user(screen_name='ArpRingh')
        self.views['public_tweets'] = api.home_timeline()
        

        return render(request,'twitter.html',self.views)




class LoginView(BaseView):
     def get(self, request):
         return render(request, 'login.html', self.views)


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword: 
            if coreUser.objects.filter(username = username).exists():
                messages.error(request,"The username is already in use.")
                return redirect('blog:register')
            elif coreUser.objects.filter(email = email).exists():
                messages.error(request, "The email is already in use.")
                return redirect('blog:register')
            else:
                user = coreUser.objects.create_user(
                    username= username,
                    email = email,
                    password = password
                        )
                user.save()
                return redirect('/')
        else:
            messages.error(request,"The password doesn't match.")
            return redirect('blog:register')

    return render(request,'register.html')
