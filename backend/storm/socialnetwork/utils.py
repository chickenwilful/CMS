def has_socialnetwork_perms(user):
    """Determines whether the user has permissions to access any socialnetwork
    views.
    
    @type user: models.User
    @param user: The user of the current request, typically C{request.user}.
    
    @rtype: bool
    @return: True if the user has permissions to access the socialnetwork views
    """
    return (user.has_perm("socialnetwork.add_socialtoken") and 
            user.has_perm("socialnetwork.change_socialtoken") and
            user.has_perm("socialnetwork.delete_socialtoken"))