from django.urls import path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('', get_schema_view(
        title="Borg Hive",
        description="Borg Hive API Schema",
        version="1"
    ), name='openapi-schema'),
]
