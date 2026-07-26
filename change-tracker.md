# Change Tracker

## [2026-07-25] Initial Local Clone & Memory Setup
- **Action**: Cloned `benny2168/home-dashboard` repository into local workspace `/Users/benny2168/Antigravity/home-dashboard-abraham`.
- **Branch**: `main`
- **Files Added**: `current-state.md`, `notes-next-session.md`, `change-tracker.md`.
- **Validation**: Verified repository structure, checked out `main` branch, git working directory clean.

## [2026-07-25] Switch Authentication to Authentik OIDC
- **Action**: Reconnected Home Dashboard authentication from Entra ID / Synology SSO to Authentik OIDC.
- **Provider Config**: Configured `Authentik` provider in `src/auth.config.ts` with issuer `https://auth.abraham16.com/application/o/dashboard`.
- **Callbacks**: Updated `src/auth.ts` `signIn` and `jwt` callbacks to process Authentik groups and upsert user profiles into Prisma database.
- **UI**: Added "Sign in with Authentik" button to `src/app/login/LoginForm.tsx`.
- **Environment**: Created `.env` and updated `.env.example` with Authentik credentials.
- **Validation**: Installed packages (`npm install`), generated Prisma client (`npx prisma generate`), and verified clean build configuration.
