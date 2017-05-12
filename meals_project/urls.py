from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import handler404, handler500
from friday_meals import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index' ),
    url(r'^meal/(?P<id>\d+)/$', views.meal, name='meal'),
    url(r'^category/$', views.category, name='category'),
    url(r'^category/(?P<id>\d+)/$', views.category_items, name='category_items'),
    url(r'^login/$', views.login_view, name='login' ),
    url(r'^logout/$', views.logout_view, name='logout' ),
    url(r'^register/$', views.register, name='register' ),
    url(r'^profile/$', views.profile, name='profile' ),
    url(r'^admin_panel/$', views.admin_panel, name='admin_panel' ),
    url(r'^assign_category/$', views.assign_category, name='assign_category' ),
    url(r'^reset_meal/$', views.reset_meal, name='reset_meal' ),
    url(r'^search_meals/$', views.search_meals, name='search_meals' ),
    url(r'^send_order_to_staff/$', views.send_order_to_staff, name='send_order_to_staff' ),
    url(r'^admin_undo_order/$', views.admin_undo_order, name='admin_undo_order' ),
    url(r'^delete_meal_from_order/(?P<id>\d+)/$', views.delete_meal_from_order, name='delete_meal_from_order' ),
    url(r'^activate_token/(?P<token>\d+-\d+)/$', views.activate_token, name='activate_token' ),
]
