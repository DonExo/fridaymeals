from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from friday_meals import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^meal/(?P<meal_id>\d+)/$', views.meal_details, name='meal'),
    url(r'^categories/$', views.categories, name='category'),
    url(r'^category/(?P<category_id>\d+)/$', views.category_items, name='category_items'),
    url(r'^login/$', views.login_view, name='login' ),
    url(r'^logout/$', views.logout_view, name='logout' ),
    url(r'^register/$', views.register, name='register' ),
    url(r'^profile/$', views.profile, name='profile' ),
    url(r'^admin-panel/$', views.admin_panel, name='admin_panel' ),
    url(r'^assign-category/$', views.assign_category, name='assign_category' ),
    url(r'^reset-meal/$', views.reset_meal, name='reset_meal' ),
    url(r'^search-meals/$', views.search_meals, name='search_meals' ),
    url(r'^send-order-to-staff/$', views.send_order_to_staff, name='send_order_to_staff' ),
    url(r'^admin-undo-order/$', views.admin_undo_order, name='admin_undo_order' ),
    url(r'^delete-meal-from-order/(?P<meal_id>\d+)/$', views.delete_meal_from_order, name='delete_meal_from_order' ),
    url(r'^activate-token/(?P<token>\d+-\d+)/$', views.activate_token, name='activate_token' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)