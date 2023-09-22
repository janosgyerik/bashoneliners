from django.contrib import admin, sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView

from oneliners import models

posts_sitemap = {
    "queryset": models.OneLiner.objects.all(),
    "date_field": "updated_dt",
}


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ['feeds', 'oneliners_newest']

    def location(self, item):
        return reverse(item)


sitemaps = {
    "blog": sitemaps.GenericSitemap(posts_sitemap, priority=0.6),
    "pages": StaticViewSitemap,
}

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', RedirectView.as_view(url='oneliners/newest/', permanent=True), name='index'),

    path('oneliners/', include('oneliners.urls')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),

    path('admin/', admin.site.urls),

    path('legal/privacy-policy', TemplateView.as_view(template_name="legal/privacy-policy.html")),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]
