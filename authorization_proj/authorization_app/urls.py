from django.urls import path

from authorization_app.views import (
    SignupAPI, LoginAPI, LogoutAPI,
    DeleteProfileSoftAPI,
    UserProfileAPI,
    Resource1API, Resource2API, Resource3API,
    AuthorizationControlGroupsAPI, AuthorizationControlUserAPI,
    AuthorizationControlAddUserInGroupAPI,
    AuthorizationControlDeleteUserInGroupAPI,
)

urlpatterns = [
    path('signup/', SignupAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('delete_profile/', DeleteProfileSoftAPI.as_view()),
    path('update_profile/', UserProfileAPI.as_view()),

    path('resource_simple/', Resource1API.as_view()),
    path('resource_vip/', Resource2API.as_view()),
    path('resource_admin/', Resource3API.as_view()),

    path('get_user_groups/', AuthorizationControlGroupsAPI.as_view()),
    path('get_user_with_user_groups/', AuthorizationControlUserAPI.as_view()),
    path('add_user_group_to_user/',
         AuthorizationControlAddUserInGroupAPI.as_view()),
    path('delete_user_group_from_user/',
         AuthorizationControlDeleteUserInGroupAPI.as_view()),

]
