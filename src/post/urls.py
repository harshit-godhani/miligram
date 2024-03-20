from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    get_post,
    create_post,
    delete_post,
    update_post,
)

urlpatterns = [
    path("", get_post),
    path("create", create_post),
    path("update", update_post),
    path("delete", delete_post),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
