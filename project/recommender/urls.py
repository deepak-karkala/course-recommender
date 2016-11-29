from django.conf.urls import url

from . import views

app_name = 'recommender'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^submitted/$', views.submitted, name='submitted')
]
