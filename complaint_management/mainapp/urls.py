from django.urls import path, include
from mainapp.views import (IndexView, ComplaintListView, UserCreateView, ComplaintCreateView, 
                           ComplaintDeleteView, ComplaintDetailView, add_comment_to_complaint, user_logout, user_login)

app_name = "mainapp"

urlpatterns = [
    path("", ComplaintListView.as_view(), name="complaint_list"),
    path("", ComplaintListView.as_view(), name="index"),
    path("complaint_detail/<int:pk>/", ComplaintDetailView.as_view(), name="complaint_detail"),
    path("user_create/", UserCreateView.as_view(), name="user_create"),
    path("complaint_create/", ComplaintCreateView.as_view(), name="complaint_create"),
    path("complaint_delete/<int:pk>/", ComplaintDeleteView.as_view(), name="complaint_delete"),
    path("complaint_detail/create_comment/<int:pk>", add_comment_to_complaint, name="create_comment"),
    path("mainapp/login", user_login, name="login"),

]
