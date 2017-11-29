from django.conf.urls import url
from . import views

from .views import list

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^homepage/$', views.HomePageView.as_view()),
    url(r'^watchlist/$', views.WatchlistPageView.as_view()),
    url(r'^generate/$', views.GeneratePageView.as_view()),
    url(r'^list/$', list),
]


