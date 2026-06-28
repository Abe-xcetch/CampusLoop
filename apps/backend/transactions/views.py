from rest_framework import status, generics, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from transactions.models import Transaction, Review, TransactionStatus
from transactions.serializers import (
    TransactionSerializer,
    TransactionCreateSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from listings.models import Listing, ListingApprovalStatus
from users.permissions import IsAdminUser


class TransactionListCreateView(generics.ListCreateAPIView):
    """
    GET /api/v1/transactions/ - List current user's transactions (buyer or seller)
    POST /api/v1/transactions/ - Initiate transaction on approved listing
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        # Admin can see all transactions
        if user.is_staff or user.is_superuser:
            return Transaction.objects.all()
        # Regular users see their own transactions (as buyer or seller)
        return Transaction.objects.filter(buyer=user) | Transaction.objects.filter(seller=user)

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        
        # Prevent buying own listing
        if listing.seller == self.request.user:
            raise serializers.ValidationError({"detail": "You cannot initiate a transaction on your own listing."})
        
        # Check if listing is sold
        if listing.approval_status == ListingApprovalStatus.SOLD:
            raise serializers.ValidationError({"detail": "This listing has already been sold."})
        
        # Check if listing is approved
        if listing.approval_status != ListingApprovalStatus.APPROVED:
            raise serializers.ValidationError({"detail": "Can only initiate transaction on approved listings."})
        
        serializer.save(
            buyer=self.request.user,
            seller=listing.seller,
            status=TransactionStatus.INITIATED
        )


class TransactionDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/transactions/{id}/ - Get transaction details
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        # Admin can see all transactions
        if user.is_staff or user.is_superuser:
            return Transaction.objects.all()
        # Regular users see their own transactions (as buyer or seller)
        return Transaction.objects.filter(buyer=user) | Transaction.objects.filter(seller=user)


class TransactionCompleteView(views.APIView):
    """
    POST /api/v1/transactions/{id}/complete/ - Seller marks transaction as completed
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only seller can complete transaction
        if transaction.seller != request.user:
            return Response(
                {"detail": "Only the seller can mark a transaction as completed."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Can only complete initiated transactions
        if transaction.status != TransactionStatus.INITIATED:
            return Response(
                {"detail": "Only initiated transactions can be marked as completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = TransactionStatus.COMPLETED
        transaction.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionVerifyView(views.APIView):
    """
    POST /api/v1/transactions/{id}/verify/ - Buyer verifies completed transaction
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only buyer can verify transaction
        if transaction.buyer != request.user:
            return Response(
                {"detail": "Only the buyer can verify a transaction."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Can only verify completed transactions
        if transaction.status != TransactionStatus.COMPLETED:
            return Response(
                {"detail": "Only completed transactions can be verified."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = TransactionStatus.VERIFIED
        transaction.save()
        
        # Mark listing as sold when transaction is verified
        listing = transaction.listing
        listing.approval_status = ListingApprovalStatus.SOLD
        listing.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionCancelView(views.APIView):
    """
    POST /api/v1/transactions/{id}/cancel/ - Buyer or seller cancels initiated transaction
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only buyer or seller can cancel transaction
        if transaction.buyer != request.user and transaction.seller != request.user:
            return Response(
                {"detail": "Only the buyer or seller can cancel a transaction."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Can only cancel initiated transactions
        if transaction.status != TransactionStatus.INITIATED:
            return Response(
                {"detail": "Only initiated transactions can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = TransactionStatus.CANCELLED
        transaction.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCreateView(generics.CreateAPIView):
    """
    POST /api/v1/transactions/{id}/review/ - Submit review after verification
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Can only review verified transactions
        if transaction.status != TransactionStatus.VERIFIED:
            return Response(
                {"detail": "Reviews can only be submitted for verified transactions."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reviewer must be a participant in the transaction
        if request.user not in {transaction.buyer, transaction.seller}:
            return Response(
                {"detail": "You must be a participant in the transaction to leave a review."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check for duplicate review
        if Review.objects.filter(transaction=transaction, reviewer=request.user).exists():
            return Response(
                {"detail": "You have already reviewed this transaction."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Auto-determine reviewee (review the other party)
        if request.user == transaction.buyer:
            reviewee = transaction.seller
        else:
            reviewee = transaction.buyer
        
        serializer.save(
            transaction=transaction,
            reviewer=request.user,
            reviewee=reviewee
        )
        
        response_serializer = ReviewSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TransactionReviewsView(generics.ListAPIView):
    """
    GET /api/v1/transactions/{id}/reviews/ - Get reviews for a transaction
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        transaction_id = self.kwargs['id']
        return Review.objects.filter(transaction_id=transaction_id)
