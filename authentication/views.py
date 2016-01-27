from django.contrib.auth import REDIRECT_FIELD_NAME, logout, login, authenticate
from django.contrib.auth.models import User, Group

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from authentication.forms import UserForm, UpdateUserForm

import json
import pdb

from rest_framework import viewsets
from rest_framework.response import Response
from authentication.serializers import UserSerializer, GroupSerializer
from mysite import settings

def signin(request):
    next = request.GET.get(REDIRECT_FIELD_NAME, '')
    if not next :
        next = settings.LOGIN_REDIRECT_URL
    if request.method == "POST":
        user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
        if user is not None:
            if user.is_active:
                print("User is valid, active and authenticated")
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            print("The username and password were incorrect.")
    stylesheets = ['login']
    return render_to_response('pages/login.html', locals(), context_instance=RequestContext(request))

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def users(request):
    accounts_active = "active"
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            userform = UserForm(request.POST)
            if userform.is_valid():
                userform.instance.set_password(request.POST['password'])
                userform.save()
        elif action == "UPDATE":
            user = User.objects.get(id=request.POST['id'])
            userform = UpdateUserForm(request.POST, instance=user)
            if userform.is_valid():
                userform.save()
        elif action == "DELETE":
            for user in User.objects.filter(id__in=json.loads(str(request.POST.get('user_id',"[]")))):
                user.delete()
        return HttpResponseRedirect('/accounts/users/')
    form = UserForm()
    users = User.objects.all()
    user_forms = {u.id:UpdateUserForm(instance=u) for u in users}
    scripts = ["users"]
    return render_to_response('pages/accounts.html', locals(), context_instance=RequestContext(request))

def update_pass(request):
    next = request.POST.get('next', '/')
    new_pass = request.POST.get('password', '')
    if new_pass:
        user = User.objects.get(id=request.user.id)
        user.set_password(new_pass)
        user.save()
    return HttpResponseRedirect(next)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def list(self, request):
        # import pdb; pdb.set_trace()
        # return Response(self.serializer_class(data=self.queryset).initial_data)
        return Response(self.get_serializer(self.queryset, many=True).data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
