from django.contrib import admin
from django.urls import include, path

from oneliners.views import oneliners_default

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', oneliners_default, name='index'),
    path('oneliners/', include('oneliners.urls')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),

    path(r'admin/', admin.site.urls),

    # path(r'^internal_error.html$', internal_error),
]
