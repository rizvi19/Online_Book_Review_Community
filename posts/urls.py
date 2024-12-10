from django.urls import path, re_path

from . import views

app_name='posts'

urlpatterns = [
    path("", views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),
    re_path(r"by/(?P<username>[-\w]+)/$",views.UserPosts.as_view(),name="for_user"),
    re_path(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    re_path(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
    # path("upvote/<int:pk>/", views.upvote_post, name="upvote"),
    # path("downvote/<int:pk>/", views.downvote_post, name="downvote"),
    # path('toggle-upvote/<int:pk>/', views.toggle_upvote, name='toggle_upvote'),
    # path('toggle-downvote/<int:pk>/', views.toggle_downvote, name='toggle_downvote'),
    path('vote/<int:post_id>/', views.vote, name='vote'),
]
