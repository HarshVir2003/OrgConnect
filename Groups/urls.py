from django.urls import path
from Groups.views import GroupsView, CommunityView, ContactView, MembersView

urlpatterns = [
    path('', GroupsView.as_view(), name='getGroups'),
    path('communities/', CommunityView.as_view(), name='getCommunities'),
    path('friends/', ContactView.as_view(), name='getContacts'),
    path('members/<int:id>', MembersView.as_view(), name='getMembers'),
    path('members/', MembersView.as_view(), name='getMembers'),
]
