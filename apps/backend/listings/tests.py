from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from listings.models import Category, Listing, ListingApproval, ListingApprovalStatus, ListingCondition
from users.models import UserRole

User = get_user_model()


class CategoryAPITests(TestCase):
    """Tests for Category CRUD operations."""

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
        self.student_user = User.objects.create_user(
            username="student",
            email="student@strathmore.edu",
            firebase_uid="student-uid",
            role=UserRole.STUDENT
        )
        self.category_data = {
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic devices"
        }

    def test_list_categories_public(self):
        """Test that anyone can list categories."""
        response = self.client.get("/api/v1/listings/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_admin_only(self):
        """Test that only admins can create categories."""
        # Unauthenticated user
        response = self.client.post("/api/v1/listings/categories/", self.category_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Student user
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post("/api/v1/listings/categories/", self.category_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1/listings/categories/", self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category_admin_only(self):
        """Test that only admins can update categories."""
        category = Category.objects.create(**self.category_data)
        
        # Student user
        self.client.force_authenticate(user=self.student_user)
        response = self.client.put(
            f"/api/v1/listings/categories/{category.id}/",
            {"name": "Updated Electronics", "slug": "electronics", "description": "Updated"}
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(
            f"/api/v1/listings/categories/{category.id}/",
            {"name": "Updated Electronics", "slug": "electronics", "description": "Updated"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_admin_only(self):
        """Test that only admins can delete categories."""
        category = Category.objects.create(**self.category_data)
        
        # Student user
        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(f"/api/v1/listings/categories/{category.id}/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/v1/listings/categories/{category.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ListingAPITests(TestCase):
    """Tests for Listing CRUD operations."""

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
        self.listing_data = {
            "title": "iPhone 13",
            "description": "Good condition iPhone 13",
            "price": 50000,
            "condition": ListingCondition.GOOD,
            "category": self.category.id
        }

    def test_student_can_create_listing(self):
        """Test that authenticated students can create listings."""
        self.client.force_authenticate(user=self.student1)
        response = self.client.post("/api/v1/listings/", self.listing_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(Listing.objects.first().seller, self.student1)
        self.assertEqual(Listing.objects.first().approval_status, ListingApprovalStatus.PENDING)

    def test_unauthenticated_cannot_create_listing(self):
        """Test that unauthenticated users cannot create listings."""
        response = self.client.post("/api/v1/listings/", self.listing_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_price_must_be_positive(self):
        """Test that price validation rejects zero or negative values."""
        self.client.force_authenticate(user=self.student1)
        invalid_data = self.listing_data.copy()
        invalid_data["price"] = 0
        response = self.client.post("/api/v1/listings/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_must_exist(self):
        """Test that listing creation requires valid category."""
        self.client.force_authenticate(user=self.student1)
        invalid_data = self.listing_data.copy()
        invalid_data["category"] = "00000000-0000-0000-0000-000000000000"
        response = self.client.post("/api/v1/listings/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pending_listing_hidden_from_marketplace(self):
        """Test that pending listings are not visible in public marketplace."""
        # Create pending listing
        listing = Listing.objects.create(
            title="Pending Item",
            description="This is pending",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.PENDING
        )

        # Public listing endpoint should not show pending listings
        response = self.client.get("/api/v1/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_approved_listing_visible(self):
        """Test that approved listings are visible in public marketplace."""
        # Create approved listing
        listing = Listing.objects.create(
            title="Approved Item",
            description="This is approved",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        # Public listing endpoint should show approved listings
        response = self.client.get("/api/v1/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], str(listing.id))

    def test_student_cannot_edit_another_students_listing(self):
        """Test that students can only edit their own listings."""
        # Create listing owned by student1
        listing = Listing.objects.create(
            title="Student1 Item",
            description="Owned by student1",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        # Student2 tries to edit
        self.client.force_authenticate(user=self.student2)
        response = self.client.put(
            f"/api/v1/listings/{listing.id}/",
            {
                "title": "Hacked Item",
                "description": "Trying to hack",
                "price": 100,
                "condition": ListingCondition.FAIR,
                "category": self.category.id
            }
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Verify listing wasn't changed
        listing.refresh_from_db()
        self.assertEqual(listing.title, "Student1 Item")

    def test_student_can_edit_own_listing(self):
        """Test that students can edit their own listings."""
        listing = Listing.objects.create(
            title="Original Title",
            description="Original description",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.put(
            f"/api/v1/listings/{listing.id}/",
            {
                "title": "Updated Title",
                "description": "Updated description",
                "price": 1500,
                "condition": ListingCondition.GOOD,
                "category": self.category.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listing.refresh_from_db()
        self.assertEqual(listing.title, "Updated Title")

    def test_admin_can_edit_any_listing(self):
        """Test that admins can edit any listing."""
        listing = Listing.objects.create(
            title="Student Item",
            description="Owned by student",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(
            f"/api/v1/listings/{listing.id}/",
            {
                "title": "Admin Edited",
                "description": "Admin changed this",
                "price": 2000,
                "condition": ListingCondition.LIKE_NEW,
                "category": self.category.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listing.refresh_from_db()
        self.assertEqual(listing.title, "Admin Edited")

    def test_search_listings(self):
        """Test search functionality."""
        Listing.objects.create(
            title="iPhone 13",
            description="Apple smartphone",
            price=50000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )
        Listing.objects.create(
            title="Samsung Galaxy",
            description="Android smartphone",
            price=45000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        # Search by title
        response = self.client.get("/api/v1/listings/?search=iPhone")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn("iPhone", response.data['results'][0]['title'])

        # Search by description
        response = self.client.get("/api/v1/listings/?search=Android")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_listings_by_category(self):
        """Test category filtering."""
        # Reuse existing electronics category from setUp, create books category
        electronics = self.category
        books = Category.objects.get_or_create(name="Books", slug="books")[0]

        Listing.objects.create(
            title="iPhone",
            description="Phone",
            price=50000,
            condition=ListingCondition.NEW,
            category=electronics,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )
        Listing.objects.create(
            title="Textbook",
            description="Book",
            price=2000,
            condition=ListingCondition.GOOD,
            category=books,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        response = self.client.get(f"/api/v1/listings/?category={electronics.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "iPhone")

    def test_filter_listings_by_price_range(self):
        """Test price range filtering."""
        Listing.objects.create(
            title="Cheap Item",
            description="Low price",
            price=1000,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )
        Listing.objects.create(
            title="Expensive Item",
            description="High price",
            price=100000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        response = self.client.get("/api/v1/listings/?min_price=5000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Expensive Item")

    def test_sort_listings_by_price(self):
        """Test sorting by price."""
        Listing.objects.create(
            title="Item 1",
            description="First",
            price=10000,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )
        Listing.objects.create(
            title="Item 2",
            description="Second",
            price=5000,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.APPROVED
        )

        response = self.client.get("/api/v1/listings/?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], "5000.00")

        response = self.client.get("/api/v1/listings/?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], "10000.00")

    def test_pagination_works(self):
        """Test pagination of listings."""
        for i in range(25):
            Listing.objects.create(
                title=f"Item {i}",
                description=f"Description {i}",
                price=1000 + i,
                condition=ListingCondition.GOOD,
                category=self.category,
                seller=self.student1,
                approval_status=ListingApprovalStatus.APPROVED
            )

        response = self.client.get("/api/v1/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Default page size
        self.assertIn('next', response.data)

    def test_my_listings_endpoint(self):
        """Test that users can see their own listings."""
        # Create listings for both students
        Listing.objects.create(
            title="Student1 Item",
            description="Owned by student1",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student1,
            approval_status=ListingApprovalStatus.PENDING
        )
        Listing.objects.create(
            title="Student2 Item",
            description="Owned by student2",
            price=2000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student2,
            approval_status=ListingApprovalStatus.PENDING
        )

        # Student1 should only see their own listings
        self.client.force_authenticate(user=self.student1)
        response = self.client.get("/api/v1/listings/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Student1 Item")


class ListingApprovalTests(TestCase):
    """Tests for listing approval workflow."""

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
        self.student_user = User.objects.create_user(
            username="student",
            email="student@strathmore.edu",
            firebase_uid="student-uid",
            role=UserRole.STUDENT
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic devices"
        )
        self.listing = Listing.objects.create(
            title="Pending Item",
            description="Needs approval",
            price=1000,
            condition=ListingCondition.NEW,
            category=self.category,
            seller=self.student_user,
            approval_status=ListingApprovalStatus.PENDING
        )

    def test_admin_can_approve_listing(self):
        """Test that admins can approve pending listings."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "approved", "notes": "Looks good"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.approval_status, ListingApprovalStatus.APPROVED)

    def test_admin_can_reject_listing(self):
        """Test that admins can reject pending listings."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "rejected", "notes": "Violates policy"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.approval_status, ListingApprovalStatus.REJECTED)

    def test_student_cannot_approve_listing(self):
        """Test that students cannot approve listings."""
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "approved", "notes": "I approve my own"}
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cannot_approve_non_pending_listing(self):
        """Test that only pending listings can be approved."""
        self.listing.approval_status = ListingApprovalStatus.APPROVED
        self.listing.save()

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "approved", "notes": "Try again"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approved_listing_becomes_visible(self):
        """Test that approved listings become visible in marketplace."""
        self.listing.approval_status = ListingApprovalStatus.PENDING
        self.listing.save()

        # Not visible initially
        response = self.client.get("/api/v1/listings/")
        self.assertEqual(len(response.data['results']), 0)

        # Admin approves
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "approved", "notes": "Approved"}
        )

        # Now visible
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/v1/listings/")
        self.assertEqual(len(response.data['results']), 1)

    def test_rejected_listing_remains_hidden(self):
        """Test that rejected listings remain hidden."""
        self.listing.approval_status = ListingApprovalStatus.PENDING
        self.listing.save()

        # Admin rejects
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "rejected", "notes": "Rejected"}
        )

        # Still not visible
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/v1/listings/")
        self.assertEqual(len(response.data['results']), 0)

    def test_approval_history_tracked(self):
        """Test that approval decisions are tracked."""
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(
            f"/api/v1/listings/{self.listing.id}/approve/",
            {"decision": "approved", "notes": "First approval"}
        )

        response = self.client.get(f"/api/v1/listings/{self.listing.id}/approvals/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['decision'], 'approved')
        self.assertEqual(response.data[0]['notes'], 'First approval')

    def test_listing_creation_creates_pending_approval(self):
        """Test that creating a listing automatically creates a pending ListingApproval."""
        listing = Listing.objects.create(
            title="Auto Approval Item",
            description="Created by student",
            price=1500,
            condition=ListingCondition.GOOD,
            category=self.category,
            seller=self.student_user,
            approval_status=ListingApprovalStatus.PENDING
        )

        approvals = ListingApproval.objects.filter(listing=listing)
        self.assertEqual(approvals.count(), 1)
        approval = approvals.first()
        self.assertEqual(approval.decision, 'pending')
        self.assertIsNone(approval.reviewed_by)
        self.assertIsNone(approval.reviewed_at)
