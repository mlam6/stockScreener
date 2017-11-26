from django.conf.urls import url
from stockScreener import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^homepage/$', views.HomePageView.as_view()),
    url(r'^watchlist/$', views.WatchlistPageView.as_view()),
    url(r'^generate/$', views.GeneratePageView.as_view()),
]
