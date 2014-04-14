from django.forms import ModelForm
from post.models import Post


class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        field = ('title', 'content', 'imageLink', 'isPublished')


class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        field = ('title', 'content', 'imageLink', 'isPublished')
