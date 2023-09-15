from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from oneliners.views import oneliners_default


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', oneliners_default, name='index'),
    path('oneliners/', include('oneliners.urls')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),

    path('admin/', admin.site.urls),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
