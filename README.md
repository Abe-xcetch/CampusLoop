# CampusLoop: Strathmore University Verified Student Marketplace

CampusLoop is a secure, trust-optimized, peer-to-peer student marketplace designed specifically for **Strathmore University**. It reduces scam occurrences to zero by enforcing university email registration, transaction-verified reputation scoring, admin-approved product listings, and fraud report tracking.

---

## 🛠️ Technology Stack

* **Frontend Web**: Next.js 14 (App Router, TypeScript, Tailwind CSS, Zustand, React Query, Axios)
* **Frontend Mobile**: React Native (Expo SDK 50, Expo Router, TypeScript, NativeWind)
* **Backend API**: Python 3.11, Django REST Framework, Celery, Redis
* **Database**: PostgreSQL 15
* **Authentication**: Firebase Authentication (ID Token Validation Backend)
* **Storage**: Firebase Storage (Secure Media Uploads)
* **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD

---

## 📁 Monorepo Workspace Directory Structure

```
CampusLoop/
├── apps/
│   ├── web/               # Next.js web application (responsive desktop view)
│   ├── mobile/            # React Native Expo app (Android-first)
│   └── backend/           # Django REST API + Celery Workers (DDD Layered architecture)
├── packages/
│   ├── shared/            # Shared TypeScript types, validators (Zod), and constants
│   └── ui/                # Component library stubs & Strathmore color tokens
├── infra/
│   └── docker/            # Docker configurations (Dockerfile.backend, Dockerfile.web)
├── docs/                  # API routes documentation & schemas
├── .github/
│   └── workflows/         # GitHub Actions CI/CD pipelines
├── docker-compose.yml     # Local orchestration configuration
├── pnpm-workspace.yaml   # Monorepo workspaces definition
├── package.json           # Monorepo package scripts
└── README.md              # Project manifest and guides (this file)
```

---

## 🗺️ Development Roadmap

### 🏁 Sprint 1: Authentication & Core Sync (COMPLETED)
* **Web & Mobile**: Setup Firebase Authentication UI. Enforce `@strathmore.edu` email registration rules.
* **Backend**: Implement Custom `FirebaseAuthentication` DRF middleware. Create database sync signals for newly registered users.
* **Database**: Setup `User` and `Verification` entities.

#### Sprint 1 Authentication Flow

CampusLoop uses Firebase Authentication for user identity management, with the Django backend handling authorization and local user profile synchronization.

**Authentication Architecture:**
- Firebase handles user registration, login, password hashing, and account recovery
- Frontend obtains Firebase ID token after successful Firebase authentication
- Frontend sends Firebase ID token to Django backend in Authorization header: `Bearer <firebase_id_token>`
- Django backend verifies the token using Firebase Admin SDK
- Backend validates email domain (`@strathmore.edu` only) and email verification status
- Backend creates or updates local User profile synced with Firebase UID
- Subsequent API requests include the Firebase ID token for authentication

**Firebase Credentials Setup:**

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Email/Password authentication in Firebase Console
3. Download the service account key (JSON file) from Project Settings > Service Accounts
4. Place the service account JSON file at `apps/backend/firebase-credentials.json` (or configure path in `.env`)
5. Add the following environment variables to your `.env` file:

```bash
FIREBASE_CREDENTIALS_PATH=apps/backend/firebase-credentials.json
FIREBASE_STORAGE_BUCKET=strathmore-marketplace.appspot.com
```

**Sprint 1 API Endpoints:**

All authentication endpoints are under `/api/v1/auth/`:

- `GET /api/v1/auth/me/` - Protected endpoint. Returns current authenticated user profile.
- `POST /api/v1/auth/register/` - Accepts Firebase ID token. Verifies token, validates @strathmore.edu email and verified status, creates or updates local User profile. Returns user profile.
- `POST /api/v1/auth/login/` - Accepts Firebase ID token. Verifies token, returns local authenticated user profile. Does not create password-based login (Firebase handles authentication).
- `POST /api/v1/auth/logout/` - Protected endpoint. Returns logout success message. Frontend/mobile must delete stored token on logout.
- `POST /api/v1/auth/password-reset/` - Accepts email. Validates @strathmore.edu domain. Returns safe success message. Does not expose whether email exists. Firebase password reset can be integrated here.
- `GET /api/v1/auth/protected-test/` - Protected endpoint used to demonstrate that unauthenticated users cannot access protected API routes.

**Access Control:**

- `IsStudent` permission class - checks if authenticated user has role "student"
- `IsAdminUser` permission class - checks if authenticated user is admin (uses Django's `is_staff` or `is_superuser`)
- Backend enforces authorization, not just frontend
- Buyer/seller are actions, not separate roles
- Admin users identified using `is_staff` or `is_superuser`

**Running Sprint 1 Tests:**

```bash
# Run all authentication tests
docker-compose exec backend python apps/backend/manage.py test users.tests.test_authentication

# Run specific test
docker-compose exec backend python apps/backend/manage.py test users.tests.test_authentication.FirebaseAuthenticationTests

# Run with verbose output
docker-compose exec backend python apps/backend/manage.py test users.tests.test_authentication --verbosity=2
```

**Important Notes:**
- Firebase handles all password hashing and account recovery
- Backend does not store passwords; only Firebase UID and profile data
- Email verification must be completed in Firebase before backend allows access
- Only @strathmore.edu email addresses are permitted for registration

### 📦 Sprint 2A Part 1: Listings and Categories API (COMPLETED)
* **Backend**: Implement Category CRUD (admin only), Listing CRUD with student/admin permissions, listing approval workflow, search/filter/sort/pagination.
* **Database**: Category, Listing, and ListingApproval entities already exist.

#### Sprint 2A Part 1 API Endpoints

All listings endpoints are under `/api/v1/listings/`:

**Category Endpoints:**
- `GET /api/v1/listings/categories/` - List all categories (public)
- `POST /api/v1/listings/categories/` - Create category (admin only)
- `GET /api/v1/listings/categories/{id}/` - Get category details (public)
- `PUT /api/v1/listings/categories/{id}/` - Update category (admin only)
- `DELETE /api/v1/listings/categories/{id}/` - Delete category (admin only)

**Listing Endpoints:**
- `GET /api/v1/listings/` - List approved listings with search, filter, sort, and pagination (public)
- `POST /api/v1/listings/` - Create listing (authenticated student only)
- `GET /api/v1/listings/{id}/` - Get listing details (public for approved, owner for pending)
- `PUT /api/v1/listings/{id}/` - Update listing (owner only if not sold)
- `DELETE /api/v1/listings/{id}/` - Delete listing (owner only if not sold)
- `GET /api/v1/listings/my/` - Get current user's listings (authenticated only)

**Listing Approval Endpoints:**
- `POST /api/v1/listings/{id}/approve/` - Approve or reject listing (admin only)
- `GET /api/v1/listings/{id}/approvals/` - Get approval history for a listing (admin only)

**Listing Approval Workflow:**
- New listings default to `pending` status
- Pending listings are hidden from public marketplace results
- Admin can approve listing (status becomes `approved`)
- Admin can reject listing with reason/comment (status becomes `rejected`)
- Approved listings become visible in public marketplace
- Rejected listings remain hidden
- Only pending listings can be approved or rejected

**Search, Filter, and Sort:**
- Search by title or description: `?search=query`
- Filter by category: `?category={category_id}`
- Filter by condition: `?condition={condition}`
- Filter by status: `?status={status}` (admin use)
- Filter by price range: `?min_price={min}&max_price={max}`
- Sort by created_at: `?ordering=created_at` or `?ordering=-created_at`
- Sort by price: `?ordering=price` or `?ordering=-price`
- Sort by title: `?ordering=title` or `?ordering=-title`
- Pagination: `?page={page}&page_size={size}` (default page_size=20, max=100)

**Access Control:**
- `IsOwnerOrAdmin` permission class - checks if authenticated user is the owner of the object or an admin
- Students can manage only their own listings
- Admin users can manage all listings
- Backend enforces authorization, not just frontend
- Category CRUD operations restricted to admins only
- Listing creation restricted to authenticated students

**Validation:**
- Price must be greater than 0
- Category must exist
- Normal users cannot change approval status (use approval endpoint)
- Only pending listings can be approved or rejected

**Running Sprint 2A Part 1 Tests:**

```bash
# Run all listings tests
docker-compose exec backend python apps/backend/manage.py test listings

# Run specific test class
docker-compose exec backend python apps/backend/manage.py test listings.tests.CategoryAPITests

# Run with verbose output
docker-compose exec backend python apps/backend/manage.py test listings --verbosity=2
```

**Important Notes:**
- Listings require admin approval before appearing in public marketplace
- Students can only edit/delete their own listings that are not sold
- Admins have full control over all listings and categories
- Search, filter, and sort functionality is built using Django REST Framework filters
- Pagination is applied to listing list views to improve performance

### 🤝 Sprint 2A Part 2: Transaction Workflow API (COMPLETED)
* **Backend**: Implement transaction initiation, status workflow, review submission with unlock conditions.
* **Database**: Transaction and Review entities already exist.

#### Sprint 2A Part 2 API Endpoints

All transaction endpoints are under `/api/v1/transactions/`:

**Transaction Endpoints:**
- `POST /api/v1/transactions/` - Initiate transaction on approved listing (authenticated student only)
- `GET /api/v1/transactions/` - List current user's transactions (buyer or seller)
- `GET /api/v1/transactions/{id}/` - Get transaction details
- `POST /api/v1/transactions/{id}/complete/` - Seller marks transaction as completed
- `POST /api/v1/transactions/{id}/verify/` - Buyer verifies completed transaction
- `POST /api/v1/transactions/{id}/cancel/` - Buyer or seller cancels initiated transaction

**Review Endpoints:**
- `POST /api/v1/transactions/{id}/review/` - Submit review after verification
- `GET /api/v1/transactions/{id}/reviews/` - Get reviews for a transaction

**Transaction Status Workflow:**
- `initiated` → `completed` → `verified`
- `initiated` → `cancelled`
- `completed` → `verified`
- Invalid status transitions are blocked
- Only seller can mark transaction as completed
- Only buyer can verify transaction after completion
- When buyer verifies transaction, listing status becomes sold

**Transaction Initiation Rules:**
- Authenticated student can initiate transaction on approved listing
- Buyer cannot initiate transaction on their own listing
- Buyer cannot initiate transaction on pending/rejected/sold listing
- When transaction is initiated, status is `initiated`
- Buyer, seller, and listing are linked correctly

**Review Unlock Conditions:**
- Review only allowed after transaction status is `verified`
- Buyer can review seller after verified transaction
- Seller can review buyer after verified transaction
- Duplicate reviews for same transaction and reviewer are blocked
- Rating must be between 1 and 5
- Users cannot review themselves
- Only transaction participants can leave reviews

**Access Control:**
- Buyer can view their own buying transactions
- Seller can view their own selling transactions
- Admin can view all transactions
- Users cannot view transactions they are not part of
- Backend enforces all transaction ownership rules

**Validation:**
- Listing availability is validated on transaction initiation
- Role permissions are validated for each action
- Status transitions are validated
- Clear error messages for invalid operations

**Running Sprint 2A Part 2 Tests:**

```bash
# Run all transaction tests
docker-compose exec backend python apps/backend/manage.py test transactions

# Run specific test class
docker-compose exec backend python apps/backend/manage.py test transactions.tests.TransactionAPITests

# Run with verbose output
docker-compose exec backend python apps/backend/manage.py test transactions --verbosity=2
```

**Important Notes:**
- Every user can act as buyer or seller depending on the transaction
- Transaction workflow ensures proper handoff lifecycle
- Reviews are only unlocked after successful transaction verification
- Listing becomes sold only when buyer verifies transaction completion
- Admin users can view all transactions but should not bypass workflow rules

### 🎨 Frontend Foundation (COMPLETED)
* **Web**: Next.js 14 with TypeScript, Tailwind CSS, Firebase client SDK, Axios
* **Design System**: Strathmore-inspired color palette, glassmorphism UI components
* **Authentication Pages**: Login, Register, Forgot Password, Email Verification
* **Dashboard**: Protected layout with stat cards and activity overview

#### Frontend Setup

The web frontend uses Next.js 14 with TypeScript and Tailwind CSS.

**Prerequisites:**
- Node.js 20+
- pnpm 8+

**Installation:**

```bash
# Navigate to web app
cd apps/web

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local
```

**Environment Variables:**

Create a `.env.local` file in `apps/web/` with the following:

```bash
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
# or for production: NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com/api/v1
```

**Running the Development Server:**

```bash
# From project root
pnpm dev:web

# Or from apps/web directory
pnpm dev
```

The frontend will be available at `http://localhost:3000`

**Frontend Architecture:**

```
apps/web/src/
├── app/              # Next.js App Router pages
│   ├── auth/         # Authentication pages
│   ├── dashboard/    # Protected dashboard
│   └── layout.tsx    # Root layout with navbar
├── components/       # Reusable UI components
│   ├── ui/          # Design system components
│   └── brand/       # Brand-specific components
├── features/        # Feature-specific modules
│   ├── auth/        # Authentication components
│   ├── listings/    # Marketplace listings
│   └── transactions/ # Transaction management
├── lib/             # Utility libraries
│   ├── firebase.ts  # Firebase client SDK setup
│   └── auth.tsx     # Authentication utilities
├── services/        # API services
│   └── apiClient.ts # Axios client with token injection
├── stores/          # State management (Zustand)
└── types/           # TypeScript type definitions
```

**Design System:**

- **Colors**: Strathmore blue (#003366) and gold (#cc9933) accents
- **Typography**: Inter (body) and Outfit (display) fonts
- **Components**: Button, Input, Card, Badge, LoadingSpinner, EmptyState, ErrorMessage
- **Style**: Glassmorphism with subtle shadows and hover effects

**Authentication Flow:**

1. User registers/logs in via Firebase Authentication
2. Firebase ID token is obtained and stored in localStorage
3. API client automatically injects token in Authorization header
4. Backend validates token and returns user profile
5. Protected routes check authentication status

**Building for Production:**

```bash
cd apps/web
pnpm build
pnpm start
```

### 📦 Sprint 2A Part 3: Marketplace Listings & Uploads (PENDING)
* **Web & Mobile**: Design listing creation forms, integrate Firebase Storage direct uploads, construct search grids with category filters.
* **Backend**: Setup category hierarchies. Implement `Listing` ORM models and serializers. Write Listing upload use cases.
* **Database**: Integrate `Listing`, `ListingMedia`, and `Category` entities.

### 🤝 Sprint 3: Transactions & Handoff Lifecycle
* **Web & Mobile**: Create buyer order request pages, seller deal confirmations, and buyer delivery logs.
* **Backend**: Build transaction status transitions use cases. Trigger push/email notifications on updates via Celery.
* **Database**: Connect `Transaction` entities mapping buyers/sellers.

### 🌟 Sprint 4: Reputation & Peer Verification
* **Web & Mobile**: Display feedback history on student profiles. Leave rating stars post-purchase.
* **Backend**: Restrict reviews validation using transaction completion checks. Calculate reputation rating averages dynamically.
* **Database**: Create `Review` and `ReputationScore` entities.

### 🛡️ Sprint 5: Admin Moderation & Analytics
* **Web**: Admin dashboard views showing reports queues and listing approval lists.
* **Backend**: Admin-only permission restrictions. Implement moderation use cases (banning users, archiving flagged listings).
* **Database**: Store `FraudReport` and `AdminAction` audit entities.

---

## 🚀 Getting Started

### Prerequisites
* [Node.js (v20+)](https://nodejs.org/)
* [pnpm (v8+)](https://pnpm.io/)
* [Docker & Docker Compose](https://www.docker.com/)

### Installation & Run instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/CampusLoop.git
   cd CampusLoop
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory using the template:
   ```bash
   cp .env.example .env
   ```
   Fill in your Firebase credentials and local DB configurations.

3. **Start the Development Servers (using Docker Compose)**:
   This boots PostgreSQL, Redis, Django API, Celery, and Next.js Web:
   ```bash
   pnpm dev:all
   ```

4. **Initialize Django Database Migrations**:
   Run database migrations inside the backend container:
   ```bash
   docker-compose exec backend python apps/backend/manage.py migrate
   ```

5. **Start the Mobile Application (Expo)**:
   Open a separate shell and run:
   ```bash
   pnpm dev:mobile
   ```
   Press `a` to run on an Android Emulator or scan the QR code to run on a physical device.

---

## 🧪 Running Tests & Checks

Test the full monorepo suite with:
```bash
pnpm test:all
```
For backend tests specifically:
```bash
docker-compose exec backend pytest apps/backend/
```
