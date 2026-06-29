# Mobile Application Feature Modules Architecture

The React Native mobile frontend uses a **Feature-Based Modular Structure** similar to the web application. This ensures that developers can easily share conceptual logic and API integrations across platforms.

## Feature Folder Blueprint

Each folder under `apps/mobile/src/features/` follows this structural layout:

```
src/features/your-feature/
├── components/          # UI components exclusive to this feature in React Native
│   ├── FeatureForm.tsx
│   └── FeatureCard.tsx
├── hooks/               # React Query or custom mobile hook wrappers
│   └── useFeatureMutation.ts
├── services/            # API services mapping (sharing core Axios client)
└── store/               # Zustand stores for tracking feature state (e.g. auth, filters)
```

---

## Shared Routing and Feature Hooks

Unlike the web app, screens in the mobile client are managed via **Expo Router** inside the `app/` folder. The components inside `app/` are lightweight controllers that load feature-specific presentation layers from `src/features/`.

### 1. [Auth Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/mobile/src/features/auth/)
* **Purpose**: Firebase login, registration, email token validation status.
* **Store**: `useMobileAuthStore` tracking native session data.

### 2. [Listings Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/mobile/src/features/listings/)
* **Purpose**: Search screen grids, camera permissions for image upload, listing status trackers.

### 3. [Transactions Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/mobile/src/features/transactions/)
* **Purpose**: Physical cash/M-Pesa payment validation prompts, delivery confirmations.

### 4. [Reputation Feature](file:///c:/Users/Xcetch/CS-project/CampusLoop/apps/mobile/src/features/reputation/)
* **Purpose**: Native star rating forms, reviews timelines.
