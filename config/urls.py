from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('src.accounts.urls')),
    path('', include('src.catalog.urls')),
    path('', include('src.favorites.urls')),
]


if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
