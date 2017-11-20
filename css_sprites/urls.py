from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^generate/$',views.generate_new_sprites,name='generate'),
        url(r'^maskPhone/',views.masknumber,name='masknumber'),
        url(r'^$',views.index,name='index'),
]
