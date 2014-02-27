from django.forms import ModelForm
from post import models
from post.models import Post


class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'title', 'isShared')


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        field = ('content', 'title', 'isShared')