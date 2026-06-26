# AiBlocks — Tech Stack & Infrastructure

> Complete technology decisions for building and deploying the AiBlocks platform.

---

## Stack Overview

| Layer | Choice | Purpose |
|---|---|---|
| **Frontend** | Next.js + Tailwind CSS | UI, routing, SEO |
| **Backend** | Next.js API Routes | Server logic, same repo |
| **Database** | Supabase (PostgreSQL) | All platform data |
| **File Storage** | Supabase Storage → AWS S3 | Zip file uploads |
| **Auth** | Clerk | Authentication |
| **Payments** | Stripe Connect | Buyer-to-seller payments |
| **Markdown** | react-markdown | README rendering |
| **Search v1** | Supabase full-text search | Text + tag filtering |
| **Search v2** | Algolia / Meilisearch | When scale demands it |
| **Hosting** | Vercel | App deployment |
| **Code Storage** | GitHub | Source code repository |

---

## Frontend

### Next.js (React)
- Industry standard for marketplaces
- Server-side rendering (SSR) for SEO — component pages must be discoverable by search engines
- Works seamlessly with Clerk auth
- Large ecosystem and community
- API Routes eliminate need for a separate backend server

### Tailwind CSS
- Utility-first styling — fast to build, easy to maintain
- No CSS file bloat
- Consistent design system out of the box

---

## Backend

### Next.js API Routes
- Lives in the same repository as the frontend
- Handles: component uploads, payment webhooks, download gating, search queries
- No separate server to manage or deploy
- Can be extracted to a standalone service later if needed

---

## Database

### Supabase (PostgreSQL)
- Fully hosted, managed PostgreSQL
- Built-in full-text search — perfect for component search feature
- Handles all platform data:
  - Users and seller profiles
  - Components and metadata
  - Tags
  - Reviews and comments
  - Stars and download counts
  - Purchase records
- Open source — can self-host later if needed
- Real-time capabilities for future features

---

## File Storage

### Phase 1: Supabase Storage
- Simple to set up, same platform as database
- Signed URLs for secure download gating (only released after payment confirmed)
- Suitable for early stage

### Phase 2: AWS S3
- Migrate when storage needs grow
- More battle-tested at scale
- CDN integration via CloudFront

---

## Authentication

### Clerk
- Fully hosted authentication platform
- Supports all required OAuth providers:
  - Google
  - Microsoft
  - Facebook
  - GitHub
- Email/password registration
- Beautiful pre-built UI components
- Free tier: up to 10,000 monthly active users
- Simple integration with Next.js

---

## Payments

### Stripe Connect
- Industry standard for marketplace payments
- Money flows directly from buyer to seller
- Platform takes 0% cut at launch
- Stripe processing fee: ~2.9% + 30¢ per transaction
- Secure download gating via webhook confirmation
- Easy to add platform fee later via Stripe configuration
- No monthly fee — pay per transaction only

---

## Markdown Rendering

### react-markdown
- Renders seller README markdown on component detail pages
- Supports code syntax highlighting
- Battle-tested, widely used
- Lightweight

---

## Search

### v1: Supabase Full-Text Search (PostgreSQL)
- Built into the database — no extra infrastructure
- Handles text search across component names and descriptions
- Tag filtering via standard SQL queries
- Sufficient for early to mid stage

### v2: Algolia or Meilisearch
- Upgrade path when search performance becomes a bottleneck
- Algolia: hosted, powerful, generous free tier
- Meilisearch: open source alternative

---

## Hosting & Deployment

### Vercel
- Purpose-built for Next.js — zero configuration
- Connects directly to GitHub repository
- Auto-deploys on every push to main branch
- Preview deployments for every pull request
- Free tier generous for early stage
- Global CDN included

### GitHub
- Source code storage and version control
- Triggers Vercel deployments automatically
- Free for public and private repositories

---

## Cloud Infrastructure Summary

| Service | Purpose | Free Tier | Paid Tier |
|---|---|---|---|
| **GitHub** | Code storage | Free | Free |
| **Vercel** | App hosting | Free | $20/month |
| **Supabase** | Database + storage | 500MB DB, 1GB storage | $25/month |
| **Clerk** | Authentication | 10,000 MAU | $25/month |
| **Stripe** | Payments | No monthly fee | ~2.9% + 30¢/transaction |

---

## Cost by Stage

| Stage | Monthly Cost |
|---|---|
| **MVP / early users** | ~$0 |
| **Growing (10k+ users)** | ~$25–50/month |
| **Scaling** | ~$100–200/month |

---

## Deployment Flow

```
Developer writes code
        ↓
   Push to GitHub
        ↓
 Vercel detects change
        ↓
  Auto-deploys to live URL
        ↓
  App reads/writes Supabase
        ↓
  Auth handled by Clerk
        ↓
  Payments handled by Stripe
```

---

## Why This Stack for AiBlocks

- **Single language** — JavaScript/TypeScript across the entire stack
- **Low ops overhead** — Vercel + Supabase means virtually no infrastructure to manage
- **Fast to ship** — MVP can be running within days
- **Scales naturally** — each layer can be upgraded independently
- **Essentially free until traction** — no upfront infrastructure costs

---

## Future Considerations (v2+)

- **Email notifications** — Resend or SendGrid for purchase confirmations, review alerts
- **Analytics** — Posthog or Plausible for usage tracking
- **AI-powered search** — Semantic search across component descriptions
- **CDN for zip files** — AWS CloudFront for faster global downloads
- **Rate limiting** — Upstash Redis for API protection

---

*Document created: June 2026*
