from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    # path('search/', views.search_view, name='search'),
    path('brewery/<str:id>', views.brewery_details, name='brewery_details'),
]