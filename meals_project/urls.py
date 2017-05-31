from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fridays/', include('friday_meals.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)