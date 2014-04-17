"""socialnetwork utility module

@author: Muhammad Fazli Bin Rosli
Matriculation Number: N1302335L
"""

from django.contrib.auth.models import Group

def has_socialnetwork_perms(user):
    """Determines whether the user has permissions to access any socialnetwork
    views.
    
    @type user: models.User
    @param user: The user of the current request, typically C{request.user}.
    
    @rtype: bool
    @return: True if the user has permissions to access the socialnetwork views
    """
    return user.groups.filter(name="CMSAdmin").exists()