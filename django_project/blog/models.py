from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class Post(models.Model,HitCountMixin):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on "{}"'.format(self.user.username,self.post)