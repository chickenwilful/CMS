from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from main.templatetags.post_permission_tags import can_create_post, can_update_post, can_delete_post
from post.forms import PostCreateForm, PostUpdateForm
from post.models import Post
from socialnetwork.socialcenter import SocialCenter


def post_retrieve(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/post_retrieve.html', {"post": post})


def post_list(request, emergency_situation_id=0):
    if int(emergency_situation_id) == 0:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.filter(type=emergency_situation_id)

    post_list = post_list.filter(Q(created_by=request.user.id) | Q(isPublished=True)).order_by("-id")

    for post in post_list:
        post.content = post.content[:280]
    return render(request, "post/post_list.html", {'post_list': post_list, 'filter_id': emergency_situation_id})


def post_create(request):
    #todo isPublished affects
    """
    Render and process a form to add a Post.
    """
    #Check permission
    if not can_create_post(request.user):
        return render(request, "main/no_permission.html")

    if not (request.POST or request.GET):
        form = PostCreateForm()
        return render(request, 'post/post_create.html', {'form': form})
    else:
        #Form POST request is submitted
        if request.POST:
            form = PostCreateForm(request.POST)
        else:
            form = PostCreateForm(request.GET)
        if form.is_valid():
            print "form valid"
            model_instance = form.save(commit=False)
            model_instance.created_by_id = request.user.id
            model_instance.created_at = timezone.now()
            model_instance.save()
            social_center = SocialCenter()
            social_center.publish(model_instance.title,
                                  model_instance.content,
                                  request.build_absolute_uri("/post/post_retrieve/%d" % model_instance.id))
            return redirect("/post/post_retrieve/%d/" % model_instance.id)
        else:
            return render(request, 'post/post_create.html', {'form': form})


def post_update(request, post_id):
    """
    Render and process a form to edit a Post
    """
    #Check permission
    if not can_update_post(request.user, Post.objects.get(pk=post_id)):
        return render(request, "main/no_permission.html")

    if not (request.POST or request.GET):
        post = get_object_or_404(Post, pk=post_id)
        form = PostUpdateForm(instance=post)
        return render(request, "post/post_update.html", {'form': form})
    else:
        # Form POST request is submitted
        post = Post.objects.get(pk=post_id)
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post.post_retrieve', args=(post_id,)))
        else:
            return HttpResponse("Fail!")


def post_delete(request, post_id):
    """
    delete a post
    """
    #Check permission
    if not can_delete_post(request.user, Post.objects.get(pk=post_id)):
        return render(request, "main/no_permission.html")

    Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('post.post_list'))


