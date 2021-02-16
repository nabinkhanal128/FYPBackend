from rest_framework import permissions

from users import models


class IsOwner(permissions.BasePermission):
    '''
Custom permission to only give the owner of the object access
'''
    message = 'You must be the owner of this object'

def has_permission(self, request, view):
    if view.action == 'list' and not request.user.is_staff:
        print('has_permission false')
        return False
    else:
        print('has_permission true')
        return True

def has_object_permission(self, request, view, obj):
    print('enter has_object_permission')
    # only allow the owner to make changes
    user = self.get_user_for_obj(obj)
    print(f'user: {user.email}')
    if request.user.is_staff:
        print('has_object_permission true: staff')
        return True
    elif view.action == 'create':
        print('has_object_permission true: create')
        return True
    elif user == request.user:
        print('has_object_permission true: owner')
        return True # in practice, an editor will have a profile
    else:
        print('has_object_permission false')
        return False

def get_user_for_obj(self, obj):
    model = type(obj)
    if model is models.Patient:
        return obj.user
    else:
        return obj.owner.user