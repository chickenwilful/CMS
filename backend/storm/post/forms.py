from django.forms import ModelForm
from post.models import Post


class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        field = ('title', 'content', 'imageLink', 'isShared')


class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        field = ('title', 'content', 'imageLink', 'isShared')
