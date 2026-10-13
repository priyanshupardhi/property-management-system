
from django.urls import path

from .views import (
    PropertyListCreateView, PropertyDetailView, UnitCreateView, UnitListView,
)

urlpatterns = [
    path(
        "properties/", PropertyListCreateView.as_view(), name="property-list-create",
    ),
    path(
        "properties/<int:pk>/", PropertyDetailView.as_view(), name="property-detail",
    ),
    path(
        "properties/<int:property_id>/units/", UnitCreateView.as_view(), name="unit-create",
    ),
    path(
        "units/", UnitListView.as_view(), name="unit-list",
    ),
]
