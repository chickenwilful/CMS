from django import template

register = template.Library()


@register.filter(name='can_list_post')
def can_list_post(user):
    """
        Permission of see post list
        Everyone can see post list
    """
    return True


@register.filter(name='can_retrieve_post')
def can_retrieve_post(user, post):
    """
        Permission of see a post retrieve
        Everyone can see a post retrieve
    """
    return True

@register.filter(name='can_create_post')
def can_create_post(user):
    return "post.post_create" in user.get_all_permissions()


@register.filter(name='can_update_post')
def can_update_post(user, post):
    ans = "post.post_create" in user.get_all_permissions()
    return ans and (user == post.created_by or user.groups.all()[0].name == "CMSAdmin")


@register.filter(name='can_delete_post')
def can_delete_post(user, post):
    ans = "post.post_delete" in user.get_all_permissions()
    return ans and (user == post.created_by or user.groups.all()[0].name == "CMSAdmin")


