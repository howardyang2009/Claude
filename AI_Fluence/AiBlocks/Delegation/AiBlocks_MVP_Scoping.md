# AiBlocks — MVP Scoping Document

> The minimum viable product definition for AiBlocks v1, v2, and v3.

---

## Philosophy

**MVP (Minimum Viable Product)** means the smallest, simplest version of AiBlocks that is still useful enough to launch and get real users.

> *"If you're not embarrassed by the first version of your product, you launched too late."*
> — Reid Hoffman, founder of LinkedIn

Rather than building all 17 pages at once (which takes months), AiBlocks launches with 8 core pages that deliver the complete core value proposition: sellers can earn, buyers can download.

---

## V1 — Must Have (Launch with these)

### Pages

| Page | Route | Reason |
|---|---|---|
| **Home Page** | `/` | First impression, discovery entry point |
| **Browse/Search Page** | `/browse` | Core functionality — find components |
| **Component Detail Page** | `/components/[id]` | Core functionality — view and download |
| **Sign Up** | `/sign-up` | Required for any user action |
| **Sign In** | `/sign-in` | Required for any user action |
| **My Downloads** | `/dashboard/downloads` | Buyers need to re-download purchases |
| **Publish Component** | `/dashboard/seller/new` | Sellers need to upload components |
| **Seller Profile** | `/sellers/[username]` | Builds trust, shows seller credibility |

**Total: 8 pages**

### Features

| Feature | Reason |
|---|---|
| **Free component upload + download** | Core value proposition |
| **Paid download via Stripe Connect** | Core monetization — without this sellers have no incentive |
| **Text search + tag filtering** | Without search, nobody finds anything |
| **Star rating** | Basic quality signal |
| **Markdown README rendering** | Components need proper documentation |
| **Clerk auth (OAuth + email/password)** | Required for any user action |
| **Seller Stripe onboarding** | Required for paid components |
| **Zip file upload (max 10MB)** | Core component delivery mechanism |

### V1 Core User Journey

```
Seller:
Sign up → Connect Stripe → Publish component (free or paid) → Share profile

Buyer:
Browse/Search → View component → Download free OR Pay → Re-download anytime
```

---

## V2 — Nice to Have (Add after launch)

### Pages

| Page | Route | Reason to Delay |
|---|---|---|
| **My Stars** | `/dashboard/stars` | Useful but not critical day one |
| **My Reviews** | `/dashboard/reviews` | No reviews yet on day one anyway |
| **Seller Dashboard** | `/dashboard/seller` | Basic stats visible on profile for now |
| **Stripe Onboarding** | `/dashboard/seller/stripe` | Can be part of publish flow in v1 |
| **Admin Dashboard** | `/admin` | Database can be managed directly early on |

### Features

| Feature | Reason to Delay |
|---|---|
| **Written reviews + comments** | Need users first before reviews matter |
| **Seller replies to reviews** | Depends on reviews existing first |
| **Tag autocomplete** | Can launch with simple free-form tags |
| **Sort by newest / most popular / most starred** | Default sort fine for small catalog |
| **Seller earnings stats** | Stripe dashboard covers this early on |
| **About / Terms / Privacy pages** | Important but not blocking launch |
| **Component edit page** | Sellers can re-publish in v1 if needed |

---

## V3 — Future (Don't think about yet)

| Feature | Reason |
|---|---|
| **AI-powered semantic search** | Complex, needs scale to justify |
| **Verified seller badge** | Needs enough sellers first |
| **Top Seller badge** | Needs enough transaction history first |
| **Email notifications** | Nice but not critical early |
| **Buyer/seller analytics dashboard** | Premature at early stage |
| **AWS S3 migration** | Only needed at serious storage scale |
| **Abuse / fraud reporting system** | Only needed with significant user base |
| **Component versioning** | Decided against in vision — revisit if users request |

---

## Version Summary

| Version | Pages | Key Addition |
|---|---|---|
| **V1 MVP** | 8 pages | Core upload, download, search, payments |
| **V2** | +5 pages | Reviews, comments, dashboards, stats |
| **V3** | +4 pages | AI search, badges, notifications, analytics |

---

## What V1 Delivers

Despite being minimal, V1 is **fully functional**:

- ✅ Sellers can publish free and paid components
- ✅ Sellers can earn money directly via Stripe
- ✅ Buyers can discover components via search and tags
- ✅ Buyers can download free components instantly
- ✅ Buyers can purchase and download paid components
- ✅ Buyers can re-download their purchases anytime
- ✅ Community can star components
- ✅ Seller profiles build trust and credibility

---

## Build Sequence Recommendation

Build V1 pages in this order:

1. **Auth** (Sign up / Sign in via Clerk) — everything depends on this
2. **Publish Component** — need content before anything else
3. **Component Detail Page** — core viewing experience
4. **Browse/Search Page** — discovery
5. **Home Page** — entry point
6. **Seller Profile** — credibility
7. **My Downloads** — buyer utility
8. **Stripe Integration** — monetization

---

*Document created: June 2026*
