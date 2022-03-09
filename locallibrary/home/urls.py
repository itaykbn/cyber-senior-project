from django.template.defaulttags import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
                  path("", views.home, name="home"),
                  path("create/select/", views.select, name="create"),
                  path("create/style/", views.style, name="style"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
