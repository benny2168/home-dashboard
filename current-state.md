# Current State

## Repository & Branch
- **Repo**: `benny2168/home-dashboard` (fork of `mtcdtech/home-dashboard`)
- **Active Branch**: `main`
- **Working Copy**: `/Users/benny2168/Antigravity/home-dashboard-abraham`

## Architecture & Technology Stack
- **Framework**: Next.js 16 (React 19)
- **Database / ORM**: Prisma ORM (`@prisma/client`, `@prisma/adapter-pg`)
- **Authentication**: NextAuth.js OIDC (`next-auth/providers/authentik`)
- **Styling**: Tailwind CSS / Vanilla CSS
- **Drag & Drop**: `@dnd-kit/core`, `@dnd-kit/sortable`
- **Deployment Target**: Docker / Portainer

## Status
- **Active Version**: `v1.10.0`
- **Performance Fixes**:
  - SSR enabled in `Dashboard.tsx` (removed component-wide `mounted` gate; initial HTML is now server-rendered).
  - Un-awaited `user.update` avatarColor write in `page.tsx` (fire-and-forget to eliminate TTFB delay).
  - Slimmed Prisma department query using `distinct: ['department']` and `where: { department: { not: null } }`.
  - Added `@next/bundle-analyzer` integration (`perf-reports/bundle-2026-08-11.html`).
- Reconnected login to Authentik OIDC (`https://auth.abraham16.com/application/o/dashboard`).
- Environment variables configured in `.env` and documented in `.env.example`.
- Dependencies installed and Prisma Client generated.
