from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from listings.models import Category, Listing, ListingApproval, ListingApprovalStatus
from listings.serializers import (
    CategorySerializer,
    ListingSerializer,
    ListingCreateSerializer,
    ListingUpdateSerializer,
    ListingApprovalSerializer,
    ListingApprovalActionSerializer,
)
from users.permissions import IsAdminUser, IsStudent, IsOwnerOrAdmin


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET /api/v1/listings/categories/ - List all categories (public)
    POST /api/v1/listings/categories/ - Create category (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/listings/categories/{id}/ - Get category details (public)
    PUT /api/v1/listings/categories/{id}/ - Update category (admin only)
    DELETE /api/v1/listings/categories/{id}/ - Delete category (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class ListingListCreateView(generics.ListCreateAPIView):
    """
    GET /api/v1/listings/ - List approved listings with search, filter, sort, pagination
    POST /api/v1/listings/ - Create listing (authenticated student only)
    """
    queryset = Listing.objects.filter(approval_status=ListingApprovalStatus.APPROVED)
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'approval_status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ListingCreateSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsStudent()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by status (for admin use)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = Listing.objects.filter(approval_status=status_filter)
        
        return queryset


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/listings/{id}/ - Get listing details (public for approved, owner for pending)
    PUT /api/v1/listings/{id}/ - Update listing (owner only if not sold)
    DELETE /api/v1/listings/{id}/ - Delete listing (owner only if not sold)
    """
    queryset = Listing.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ListingUpdateSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [AllowAny()]

    def get_queryset(self):
        # Non-authenticated users can only see approved listings
        if not self.request.user or not self.request.user.is_authenticated:
            return Listing.objects.filter(approval_status=ListingApprovalStatus.APPROVED)
        
        # Authenticated users can see their own listings regardless of status
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Listing.objects.all()
        
        return Listing.objects.filter(
            approval_status=ListingApprovalStatus.APPROVED
        ) | Listing.objects.filter(seller=self.request.user)


class MyListingsView(generics.ListAPIView):
    """
    GET /api/v1/listings/my/ - Get current user's listings (authenticated only)
    """
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'approval_status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)


class ListingApprovalView(APIView):
    """
    POST /api/v1/listings/{id}/approve/ - Approve or reject listing (admin only)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, id):
        try:
            listing = Listing.objects.get(id=id)
        except Listing.DoesNotExist:
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if listing.approval_status != ListingApprovalStatus.PENDING:
            return Response(
                {"detail": "Only pending listings can be approved or rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ListingApprovalActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        decision = serializer.validated_data['decision']
        notes = serializer.validated_data.get('notes', '')

        approval = ListingApproval.objects.create(
            listing=listing,
            reviewed_by=request.user,
            decision=decision,
            notes=notes
        )

        response_serializer = ListingApprovalSerializer(approval)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ListingApprovalHistoryView(generics.ListAPIView):
    """
    GET /api/v1/listings/{id}/approvals/ - Get approval history for a listing (admin only)
    """
    serializer_class = ListingApprovalSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

    def get_queryset(self):
        listing_id = self.kwargs['id']
        return ListingApproval.objects.filter(listing_id=listing_id)
