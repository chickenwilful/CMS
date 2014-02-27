from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from post.forms import PostEditForm, PostAddForm
from post.models import Post


def create(request):
    return render(request, "post/create.html")


def post_retrieve(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/post_retrieve.html', {"post": post})


def post_list(request):
    post_list = Post.objects.all()
    return render(request, "post/post_list.html", {'post_list': post_list})


def post_create(request):
    """
    Render and process a form to add a Post.
    """
    if not (request.POST or request.GET):
        form = PostAddForm()
        return render(request, 'post/post_create.html', {'form': form, 'action': ""})
    else:
        #Form POST request is submitted
        form = PostAddForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_by_id = request.user.id
            model_instance.created_at = timezone.now()
            model_instance.save()
            return redirect("post.post_list")
        else:
            return render(request, 'post/post_create.html', {'form': form, 'action': ""})


def post_update(request, post_id):
    """
    Render and process a form to edit a Post
    """
    if not (request.POST or request.GET):
        post = get_object_or_404(Post, pk=post_id)
        form = PostEditForm(instance=post)
        return render(request, "post/post_update.html", {'form': form, 'action': ''})
    else:
        # Form POST request is submitted
        post = Post.objects.get(pk=post_id)
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post.post_retrieve', args=(post_id,)))
        else:
            return HttpResponse("Fail!")


def post_delete(request, post_id):
    """
    delete a post
    """
    Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('post.post_list'))


