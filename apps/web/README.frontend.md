# CampusLoop Web (Frontend)

This folder contains the Next.js + TypeScript frontend for CampusLoop.

Quick start:


1. From workspace root, install dependencies with pnpm and then run the web app:

```bash
pnpm install
pnpm --filter web dev
```

2. Environment

Copy `.env.local.example` to `.env.local` and fill Firebase config values.

Notes:
- UI uses Tailwind CSS and a design system under `src/components/ui` and `src/components/brand`.
- Auth uses Firebase client (`src/lib/firebase.ts`) for email/password flows. After login a Firebase ID token is POSTed to `POST /auth/login/`.
- API client is `src/services/apiClient.ts` and uses axios. Set `NEXT_PUBLIC_API_BASE_URL` in env.

