from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path("", views.home, name="home"),
                  path("create/", views.create, name="create"),
                  path("messenger/", views.messenger, name="messenger")
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
