from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from transactions.models import Transaction, Review, TransactionStatus
from listings.models import Category, Listing, ListingApprovalStatus, ListingCondition
from users.models import UserRole

User = get_user_model()


class TransactionAPITests(TestCase):
    """Tests for Transaction API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@strathmore.edu",
            firebase_uid="admin-uid",
            role=UserRole.ADMIN,
            is_staff=True,
            is_superuser=True
        )
        self.student1 = User.objects.create_user(
            username="student1",
            email="student1@strathmore.edu",
            firebase_uid="student1-uid",
            role=UserRole.STUDENT
        )
        self.student2 = User.objects.create_user(
            username="student2",
            email="student2@strathmore.edu",
            firebase_uid="student2-uid",
            role=UserRole.STUDENT
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic devices"
        )
        self.approved_listing = Listing.objects.create(
            title="iPhone 13",
            description="Good condition",
            price=50000,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.APPROVED
        )
        self.pending_listing = Listing.objects.create(
            title="Pending Item",
            description="Needs approval",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.PENDING
        )
        self.rejected_listing = Listing.objects.create(
            title="Rejected Item",
            description="Was rejected",
            price=2000,
            condition=ListingCondition.FAIR,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.REJECTED
        )
        self.sold_listing = Listing.objects.create(
            title="Sold Item",
            description="Already sold",
            price=3000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.SOLD
        )

    def test_buyer_can_initiate_transaction_on_approved_listing(self):
        """Test that buyer can initiate transaction on approved listing."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": self.approved_listing.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.buyer, self.student1)
        self.assertEqual(transaction.seller, self.student2)
        self.assertEqual(transaction.status, TransactionStatus.INITIATED)

    def test_buyer_cannot_buy_own_listing(self):
        """Test that buyer cannot initiate transaction on their own listing."""
        my_listing = Listing.objects.create(
            title="My Item",
            description="Owned by me",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": my_listing.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("own listing", response.data['detail'].lower())

    def test_buyer_cannot_buy_pending_listing(self):
        """Test that buyer cannot initiate transaction on pending listing."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": self.pending_listing.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("approved", response.data['detail'].lower())

    def test_buyer_cannot_buy_rejected_listing(self):
        """Test that buyer cannot initiate transaction on rejected listing."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": self.rejected_listing.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("approved", response.data['detail'].lower())

    def test_buyer_cannot_buy_sold_listing(self):
        """Test that buyer cannot initiate transaction on sold listing."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": self.sold_listing.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("sold", response.data['detail'].lower())

    def test_unauthenticated_cannot_initiate_transaction(self):
        """Test that unauthenticated users cannot initiate transactions."""
        response = self.client.post(
            "/api/v1/transactions/",
            {"listing": self.approved_listing.id}
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_seller_can_mark_transaction_completed(self):
        """Test that seller can mark transaction as completed."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student2)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, TransactionStatus.COMPLETED)

    def test_buyer_cannot_mark_transaction_completed(self):
        """Test that buyer cannot mark transaction as completed."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, TransactionStatus.INITIATED)

    def test_only_initiated_transaction_can_be_completed(self):
        """Test that only initiated transactions can be marked as completed."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )
        
        self.client.force_authenticate(user=self.student2)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buyer_can_verify_completed_transaction(self):
        """Test that buyer can verify completed transaction."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/verify/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, TransactionStatus.VERIFIED)

    def test_seller_cannot_verify_transaction(self):
        """Test that seller cannot verify transaction."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )
        
        self.client.force_authenticate(user=self.student2)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/verify/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_completed_transaction_can_be_verified(self):
        """Test that only completed transactions can be verified."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/verify/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verifying_transaction_marks_listing_as_sold(self):
        """Test that verifying transaction marks listing as sold."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )
        
        self.assertEqual(self.approved_listing.approval_status, ListingApprovalStatus.APPROVED)
        
        self.client.force_authenticate(user=self.student1)
        self.client.post(f"/api/v1/transactions/{transaction.id}/verify/")
        
        self.approved_listing.refresh_from_db()
        self.assertEqual(self.approved_listing.approval_status, ListingApprovalStatus.SOLD)

    def test_buyer_or_seller_can_cancel_initiated_transaction(self):
        """Test that buyer or seller can cancel initiated transaction."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        # Buyer cancels
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, TransactionStatus.CANCELLED)

    def test_third_party_cannot_cancel_transaction(self):
        """Test that third party cannot cancel transaction."""
        student3 = User.objects.create_user(
            username="student3",
            email="student3@strathmore.edu",
            firebase_uid="student3-uid",
            role=UserRole.STUDENT
        )
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=student3)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_initiated_transaction_can_be_cancelled(self):
        """Test that only initiated transactions can be cancelled."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(f"/api/v1/transactions/{transaction.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buyer_can_view_own_transactions(self):
        """Test that buyer can view their own transactions."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.get("/api/v1/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(transaction.id))

    def test_seller_can_view_own_transactions(self):
        """Test that seller can view their own transactions."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student2)
        response = self.client.get("/api/v1/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(transaction.id))

    def test_admin_can_view_all_transactions(self):
        """Test that admin can view all transactions."""
        Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/v1/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_cannot_view_others_transactions(self):
        """Test that users cannot view transactions they are not part of."""
        student3 = User.objects.create_user(
            username="student3",
            email="student3@strathmore.edu",
            firebase_uid="student3-uid",
            role=UserRole.STUDENT
        )
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=student3)
        response = self.client.get("/api/v1/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_can_view_own_transaction_detail(self):
        """Test that user can view their own transaction detail."""
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.get(f"/api/v1/transactions/{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(transaction.id))

    def test_user_cannot_view_others_transaction_detail(self):
        """Test that user cannot view transaction they are not part of."""
        student3 = User.objects.create_user(
            username="student3",
            email="student3@strathmore.edu",
            firebase_uid="student3-uid",
            role=UserRole.STUDENT
        )
        transaction = Transaction.objects.create(
            listing=self.approved_listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.INITIATED
        )
        
        self.client.force_authenticate(user=student3)
        response = self.client.get(f"/api/v1/transactions/{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewAPITests(TestCase):
    """Tests for Review API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.student1 = User.objects.create_user(
            username="student1",
            email="student1@strathmore.edu",
            firebase_uid="student1-uid",
            role=UserRole.STUDENT
        )
        self.student2 = User.objects.create_user(
            username="student2",
            email="student2@strathmore.edu",
            firebase_uid="student2-uid",
            role=UserRole.STUDENT
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic devices"
        )
        self.listing = Listing.objects.create(
            title="iPhone 13",
            description="Good condition",
            price=50000,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.APPROVED
        )
        self.verified_transaction = Transaction.objects.create(
            listing=self.listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.VERIFIED
        )
        self.completed_transaction = Transaction.objects.create(
            listing=self.listing,
            buyer=self.student1,
            seller=self.student2,
            status=TransactionStatus.COMPLETED
        )

    def test_review_only_allowed_after_verified_transaction(self):
        """Test that review can only be submitted for verified transactions."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            f"/api/v1/transactions/{self.completed_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 5,
                "comment": "Great seller!"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("verified", response.data['detail'].lower())

    def test_buyer_can_review_seller_after_verification(self):
        """Test that buyer can review seller after verified transaction."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 5,
                "comment": "Great seller!"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.reviewer, self.student1)
        self.assertEqual(review.reviewee, self.student2)
        self.assertEqual(review.rating, 5)

    def test_seller_can_review_buyer_after_verification(self):
        """Test that seller can review buyer after verified transaction."""
        self.client.force_authenticate(user=self.student2)
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student1.id,
                "rating": 4,
                "comment": "Good buyer"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_duplicate_review_is_blocked(self):
        """Test that duplicate review for same transaction and reviewer is blocked."""
        Review.objects.create(
            transaction=self.verified_transaction,
            reviewer=self.student1,
            reviewee=self.student2,
            rating=5,
            comment="First review"
        )
        
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 4,
                "comment": "Second review"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already reviewed", response.data['detail'].lower())

    def test_rating_outside_1_to_5_is_rejected(self):
        """Test that rating outside 1-5 range is rejected."""
        self.client.force_authenticate(user=self.student1)
        
        # Test rating 0
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 0,
                "comment": "Invalid rating"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test rating 6
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 6,
                "comment": "Invalid rating"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_review_themselves(self):
        """Test that user cannot review themselves."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student1.id,
                "rating": 5,
                "comment": "Self review"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_transaction_participant_can_review(self):
        """Test that only transaction participants can leave reviews."""
        student3 = User.objects.create_user(
            username="student3",
            email="student3@strathmore.edu",
            firebase_uid="student3-uid",
            role=UserRole.STUDENT
        )
        
        self.client.force_authenticate(user=student3)
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 5,
                "comment": "Not a participant"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_submit_review(self):
        """Test that unauthenticated users cannot submit reviews."""
        response = self.client.post(
            f"/api/v1/transactions/{self.verified_transaction.id}/review/",
            {
                "reviewee": self.student2.id,
                "rating": 5,
                "comment": "No auth"
            }
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
