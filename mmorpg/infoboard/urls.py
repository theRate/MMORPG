from django.urls import path

from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<int:pk>', PostDetailView.as_view(), name='showpost'),
    path('addpost', PostCreateView.as_view(), name='addpost'),
    path('updatepost/<int:pk>', PostUpdateView.as_view(), name='updatepost'),
    path('deletepost/<int:pk>', PostDeleteView.as_view(), name='deletepost'),
    path('checkresps', ResponseListView.as_view(), name='checkresps'),
    path('approveresp/<int:pk>', approve_response, name='approveresp'),
    path('deleteresp/<int:pk>', delete_response, name='deleteresp'),
]
