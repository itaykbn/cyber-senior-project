from django.template.defaulttags import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
                  path("", views.home, name="home"),
                  path("create/select/", views.select, name="create"),
                  path("profile/<username>", views.profile, name="profile"),
                  path("profile/<username>/edit/", views.edit_profile, name="edit profile"),
                  path("ajax_request/", views.ajax_query, name="load images"),
                  path("posts/<post_id>", views.redirect_to_post_page, name="posts"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
