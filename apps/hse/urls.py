from django.conf.urls import url
from . import views

urlpatterns = [
        #url(r'^$', views.index, name='index'),
        #url(r'^$', views.StuffListView.as_view(), name = 'stuffall'),
        url(r'^$', views.StuffInListView.as_view(), name = 'stuffin'),

        url(r'^stuffall/', views.StuffRescuedListView.as_view(), name = 'stuffall'),
        #url(r'^stuffin/', views.StuffInListView.as_view(), name = 'stuffin'),
        url(r'^stuffunknown/', views.StuffUnknownListView.as_view(), name = 'stuffunknown'),
        url(r'^stuffdetails/(?P<pk>\d+)$', views.StuffDetailView.as_view(), name='stuff-detail'),
        url(r'^stuffdetailsunknown/(?P<pk>\d+)$', views.StuffUnknownDetailView.as_view(), name='stuff-detailunknown'),
]
