# CampusLoop API Endpoint Specifications

All API routes are versioned and start with the prefix `/api/v1`.

Authentication requires sending a valid Firebase ID Token in the request header:
`Authorization: Bearer <firebase_token>`

---

## 1. Authentication Paths (`/auth`)
*Endpoints to manage user sessions and registration sync.*

### `POST /auth/register`
* **Description**: Syncs a user profile immediately after they sign up in Firebase.
* **Payload**:
  ```json
  {
    "email": "student@strathmore.edu",
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
* **Response**: `201 Created`
* **Access**: Open (Firebase token parsed dynamically to resolve Firebase UID)

---

## 2. User Paths (`/users`)
*Managing student profile structures and verification statuses.*

### `GET /users/me`
* **Description**: Get currently logged-in student's information (including reputation stats).
* **Response**: `200 OK` + `UserProfileSerializer`

### `PUT /users/me`
* **Description**: Update profile avatar or phone number.
* **Payload**:
  ```json
  {
    "avatarUrl": "https://storage...",
    "phoneNumber": "+254712345678"
  }
  ```
* **Response**: `200 OK`

### `GET /users/<str:id>/profile`
* **Description**: Fetch public student profiles to verify trust before trading.
* **Response**: `200 OK`

---

## 3. Marketplace Listing Paths (`/listings`)
*Creating, updating, and filtering student goods listings.*

### `GET /listings`
* **Description**: Get active listings with search queries, category filters, and sorting.
* **Query Params**:
  * `search`: Search text index (e.g. `textbook`)
  * `category`: slug string filter (e.g. `electronics-gadgets`)
  * `price_min` / `price_max`: Numeric bounds
* **Response**: `200 OK` + List of listings

### `POST /listings`
* **Description**: Creates a new product listing. Placed in `PENDING_APPROVAL` status by default.
* **Payload**:
  ```json
  {
    "title": "Calculus 9th Edition Textbook",
    "description": "Like-new condition, no markings or torn pages.",
    "price": 1500.00,
    "condition": "LIKE_NEW",
    "categoryId": "48b68832-6bfb-4819-bf95-0211516e87f8",
    "mediaUrls": ["https://storage..."]
  }
  ```
* **Response**: `201 Created`

### `GET /listings/<int:id>`
* **Description**: Fetch detailed listing parameters.
* **Response**: `200 OK`

---

## 4. Transaction Paths (`/transactions`)
*Orchestrates the order hand-off lifecycle.*

### `POST /transactions`
* **Description**: Initiates a request to buy a product. Sends a notification to the seller.
* **Payload**:
  ```json
  {
    "listingId": 12
  }
  ```
* **Response**: `201 Created`

### `POST /transactions/<int:id>/confirm`
* **Description**: Called by the seller to confirm item availability and coordinate delivery/hand-off.
* **Response**: `200 OK`

### `POST /transactions/<int:id>/complete`
* **Description**: Called by the buyer to confirm receipt of the item and finalize transaction. Triggers eligibility to submit reviews.
* **Response**: `200 OK`

---

## 5. Reputation Paths (`/reputation`)
*Verified rating and feedback logs.*

### `POST /reputation/reviews`
* **Description**: Leave feedback on a seller post-completion.
* **Payload**:
  ```json
  {
    "transactionId": 105,
    "rating": 5,
    "comment": "Excellent seller, item was in perfect shape."
  }
  ```
* **Response**: `201 Created`

---

## 6. Fraud Report Paths (`/reports`)
*User moderation mechanisms.*

### `POST /reports`
* **Description**: File a report against a seller or flag a suspect listing.
* **Payload**:
  ```json
  {
    "reportedListingId": 12,
    "reason": "FRAUD_SCAM",
    "details": "Seller is demanding advance payment via M-Pesa."
  }
  ```
* **Response**: `201 Created`

---

## 7. Admin Moderation Paths (`/admin`)
*Back-office dashboards for student admins.*

### `GET /admin/listings/pending`
* **Description**: Fetch list of listings waiting for approval.
* **Access**: Admin only

### `POST /admin/listings/<int:id>/approve`
* **Description**: Approve listing, moving status to `ACTIVE`.
* **Access**: Admin only

### `POST /admin/users/<str:user_id>/ban`
* **Description**: Deactivates a user's account and labels their active listings as `ARCHIVED`.
* **Access**: Admin only
