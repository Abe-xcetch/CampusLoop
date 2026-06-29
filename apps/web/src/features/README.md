# Web Application Feature Modules Architecture

The Next.js frontend uses a **Feature-Based Modular Structure** to keep components, state management, hooks, and services organized around specific business domains.

## Feature Folder Blueprint

Each folder under `apps/web/src/features/` follows this structural layout:

```
src/features/your-feature/
├── components/          # UI components exclusive to this feature
│   ├── FeatureForm.tsx
│   └── FeatureCard.tsx
├── hooks/               # Custom hooks (e.g. React Query mutations/queries)
│   ├── useFeatureQuery.ts
│   └── useFeatureMutation.ts
├── services/            # Axios API client functions for backend interaction
│   └── api.ts
├── store/               # Zustand state stores (if feature-specific state is needed)
│   └── useFeatureStore.ts
├── types.ts             # Feature-specific TypeScript declarations
└── index.ts             # Public API entry point for the feature
```

---

## Modular Breakdown

### 1. [Auth Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/auth/)
* **Purpose**: Student login, signup validation, email verification stage, password reset, Firebase Auth sync.
* **Key State**: Firebase ID Token, User Profile.
* **Store**: `useAuthStore` managing session and current user.

### 2. [Listings Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/listings/)
* **Purpose**: Listing search, category filters, listing creation form, image upload to Firebase Storage, detail view.
* **Key Components**: `ListingCard`, `ListingGrid`, `ListingCreateForm`, `FilterPanel`.
* **Hooks**: `useListings`, `useCreateListing`, `useApproveListing`.

### 3. [Transactions Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/transactions/)
* **Purpose**: Initiating transactions, managing statuses (Initiated -> Confirmed -> Completed), chat or physical meet-up guidelines.
* **Key Components**: `TransactionProgress`, `TransactionActions`, `TransactionHistoryList`.
* **Hooks**: `useTransactionDetails`, `useUpdateTransactionStatus`.

### 4. [Reputation Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/reputation/)
* **Purpose**: Leaving feedback after a transaction, viewing seller ratings, calculating completion rate.
* **Key Components**: `RatingStars`, `ReviewList`, `SubmitReviewModal`.
* **Hooks**: `useUserReputation`, `useSubmitReview`.

### 5. [Reports Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/reports/)
* **Purpose**: Reporting scam listings, policy violations, or suspicious user accounts.
* **Key Components**: `ReportListingModal`, `ReportUserModal`, `ReportSuccess`.
* **Hooks**: `useSubmitReport`.

### 6. [Admin Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/web/src/features/admin/)
* **Purpose**: Back-office dashboard for student moderators. Approve pending listings, ban fraudulent users, view platform metrics.
* **Key Components**: `ModerationQueue`, `FraudInvestigationPanel`, `AnalyticsChart`.
* **Hooks**: `useAdminDashboardStats`, `useModerateListing`.
