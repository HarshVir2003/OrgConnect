from django.urls import path
from Groups.views import GroupsView, CommunityView, ContactView, MembersView

urlpatterns = [
    path('', GroupsView.as_view(), name='getGroups'),
    path('communitys/', CommunityView.as_view(), name='getCommunities'),
    path('friends/', ContactView.as_view(), name='getContacts'),
    path('members/', MembersView.as_view(), name='getMembers')

]
