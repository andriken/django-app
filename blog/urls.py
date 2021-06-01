from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
        views.post_detail, name='post_detail'),
    path('<post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('privacy-policy-and-disclaimer/', views.privacy_disclaimer, name="privacy-disclaimer"),
    path('gdpr-privacy-policy/', views.gdpr_policy, name="gdpr-policy")
]