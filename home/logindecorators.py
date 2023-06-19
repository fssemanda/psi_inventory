
from django.shortcuts import redirect
from django.contrib.auth import decorators
from django.http import HttpResponse

def unauthorizedUser_func(view_function):

    def wrapper_function(request, *args, ** kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_function(request,*args, **kwargs)

    return wrapper_function

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            staffrole=None
            #
            # if request.user.groups.exists():
            #
            #     group = request.user.groups.all()[0].name

            if request.user.staff.staffrole in allowed_roles:
                print(request.user.staff.staffrole)
            #if group in allowed_roles:

                return view_func(request, *args, **kwargs)

            else:

                return redirect('notauthorized')

        return wrapper_func
    return decorator

def admin_only(view_func):

    '''Admin Only function decorator allowing admin/approver only to be redirected to home dashboard'''
    def wrapper_func(request, *args, **kwargs):

        group=None

        if request.user.groups.exists():

            group = request.user.groups.all()[0].name

        if group == 'staff':
            return redirect('/staff/'+ request.user.staff.Username)

        if group == 'supplychain':
             return redirect('/warehouse/user/'+ request.user.staff.Username)

        # if group == 'Finance' or group == 'IT':
        #      return redirect('/requisitions/approvalitems')

        if group == 'IT' or group == 'Finance':

            return view_func(request, *args, **kwargs)

    return wrapper_func
