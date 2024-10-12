from django.shortcuts import render, HttpResponse
from Groups.models import Community, Group, Contacts


# Create your views here.
def vv(request):
    group = Group.objects.all()[0]
    print(group)
    members = group.get_members()
    return HttpResponse(members)
