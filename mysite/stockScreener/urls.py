from django.conf.urls import url
from . import views

from .views import list

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^homepage/$', views.homepage, name="homepage"),
    url(r'^watchlist/$', views.WatchlistPageView.as_view()),
    url(r'^generate/$', views.generate),
    url(r'^list/$', list),
]


