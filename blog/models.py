from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User

# Ckeditor
# TimeZone
# Taggit
from taggit.managers import TaggableManager
# Reverse
from django.urls import reverse
# Create your models here.



    
STATUS_CAT = (('active', 'active'), ('', 'default'))

class Category(models.Model):
    name = models.CharField(max_length = 300)
    slug = models.CharField(max_length = 300)
    status = models.CharField(choices = STATUS_CAT, blank=True, max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length = 300)
    slug = models.CharField(max_length = 300)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
        return self.name


# Model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


# Post model
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft',  'Draft'),
    ('published', 'Published'),
            )

    SECTION = (
            ('home','Home'),
            ('popular', 'Popular'),
            ('recent', 'Recent'),
            ('comment', 'Comment'),

            )


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
       
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
   
    section = models.CharField(max_length=200,choices= SECTION)
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d')
   # excerpt = models.TextField() 
    
    excerpt = RichTextUploadingField()
    #body= models.TextField()
    #body for detail view of post
    body= RichTextUploadingField()

    tags = TaggableManager()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')


    class Meta:
        ordering = ('-publish',)

        def __str__(self):
            return self.title

    objects = models.Manager() # The default manager
    published = PublishedManager() # Our custom manager


    def get_absolute_url(self):
        return reverse('blog:single',args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)





# comment model
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self",null=True,blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


class Contact(models.Model):
    name = models.CharField(max_length = 400)
    email = models.EmailField(max_length = 400, blank=True)
    subject = models.CharField(max_length = 400)
    message = models.TextField()


    def __str__(self):
        return self.name
