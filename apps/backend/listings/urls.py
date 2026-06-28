from django.urls import path
from listings.views import (
    CategoryListCreateView,
    CategoryDetailView,
    ListingListCreateView,
    ListingDetailView,
    MyListingsView,
    ListingApprovalView,
    ListingApprovalHistoryView,
)

urlpatterns = [
    # Category endpoints
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:id>/", CategoryDetailView.as_view(), name="category-detail"),
    
    # Listing endpoints
    path("", ListingListCreateView.as_view(), name="listing-list-create"),
    path("<uuid:id>/", ListingDetailView.as_view(), name="listing-detail"),
    path("my/", MyListingsView.as_view(), name="my-listings"),
    
    # Approval endpoints
    path("<uuid:id>/approve/", ListingApprovalView.as_view(), name="listing-approve"),
    path("<uuid:id>/approvals/", ListingApprovalHistoryView.as_view(), name="listing-approval-history"),
]
