from django.urls import path
from transactions.views import (
    TransactionListCreateView,
    TransactionDetailView,
    TransactionCompleteView,
    TransactionVerifyView,
    TransactionCancelView,
    ReviewCreateView,
    TransactionReviewsView,
)

urlpatterns = [
    # Transaction endpoints
    path("", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("<uuid:id>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("<uuid:id>/complete/", TransactionCompleteView.as_view(), name="transaction-complete"),
    path("<uuid:id>/verify/", TransactionVerifyView.as_view(), name="transaction-verify"),
    path("<uuid:id>/cancel/", TransactionCancelView.as_view(), name="transaction-cancel"),
    
    # Review endpoints
    path("<uuid:id>/review/", ReviewCreateView.as_view(), name="transaction-review"),
    path("<uuid:id>/reviews/", TransactionReviewsView.as_view(), name="transaction-reviews"),
]
