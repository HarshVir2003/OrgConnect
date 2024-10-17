from django.urls import path
from Groups.views import GroupsView, CommunityView, ContactView

urlpatterns = [
    path('', GroupsView.as_view(), name='getGroups'),
    path('communitys/', CommunityView.as_view(), name='getCommunities'),
    path('friends/', ContactView.as_view(), name='getContacts')

]
