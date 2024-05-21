from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    get_post,
    create_post,
    delete_post,
    update_post,
    PostImageview,
    # scrape_example_domain,
    PostCommentView,
)

urlpatterns = [
    path("", get_post),
    path("create", create_post),
    path("update", update_post),
    path("delete", delete_post),
    path("image", PostImageview.as_view()),
    # path("scrape", scrape_example_domain),
    path("postcomment", PostCommentView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
