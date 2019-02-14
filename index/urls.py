from django.conf.urls import url
from.views import *
urlpatterns=[
    url(r'^$',index_views),
    url(r'^login/$',login_views),
    url(r'^register/$',register_views),

]
urlpatterns +=[
    url(r'^check_uphone/$',check_uphone_views),
    url(r'^check_login/$',check_login_views),
    url(r'^check_logout/$',logout_views),
    url(r'^type_goods/$',type_goods_views),
]
