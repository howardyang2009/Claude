# AiBlocks — Page & Feature Mapping

> Complete map of every page in the AiBlocks platform, organized by user type and access level.

---

## Public Pages (No login required)

### 1. Home Page `/`
- Hero section — what is AiBlocks
- Featured/trending components
- Popular tags
- Search bar
- Call to action (Browse, Publish)

### 2. Browse/Search Page `/browse`
- Search bar
- Tag filter sidebar
- Component cards grid (name, author, price, stars, downloads, ecosystem)
- Sort by: newest, most downloaded, most starred

### 3. Component Detail Page `/components/[id]`
- Component name, description
- Rendered markdown README
- Metadata (author, ecosystem, tags, price, downloads, stars)
- Star button
- Download / Buy button
- Verified buyer reviews section
- Open comments section

### 4. Seller Profile Page `/sellers/[username]`
- Avatar, name, bio, links
- Stats (total components, downloads, stars)
- Their published components grid

### 5. Static Pages
- `/about` — what is AiBlocks
- `/terms` — terms of service
- `/privacy` — privacy policy

---

## Auth Pages (Handled by Clerk)

### 6. Sign Up `/sign-up`
- OAuth buttons (Google, Microsoft, Facebook, GitHub)
- Email/password form

### 7. Sign In `/sign-in`
- OAuth buttons
- Email/password form

---

## Buyer Pages (Login required)

### 8. My Downloads `/dashboard/downloads`
- All purchased/downloaded components
- Re-download zip button

### 9. My Stars `/dashboard/stars`
- All starred components

### 10. My Reviews `/dashboard/reviews`
- Reviews the buyer has written

---

## Seller Pages (Login required)

### 11. Seller Dashboard `/dashboard/seller`
- Overview stats (total components, downloads, earnings)
- List of published components
- Quick actions (publish new, edit existing)

### 12. Publish Component `/dashboard/seller/new`
- Form fields:
  - Component name
  - Short description
  - Ecosystem tags (Claude, GPT, Gemini, Deepseek, etc.)
  - Free-form tags with autocomplete
  - Price (free or set amount)
  - Markdown README editor with live preview
  - Zip file upload (max 10MB)
- Submit / Publish button

### 13. Edit Component `/dashboard/seller/[id]/edit`
- Same form as publish, pre-filled with existing data
- Update / Save button

### 14. Stripe Onboarding `/dashboard/seller/stripe`
- Connect Stripe account
- View payout status

---

## Admin Pages (Platform owner only)

### 15. Admin Dashboard `/admin`
- Total users, components, transactions
- Flag/remove abusive components
- Basic platform health stats

---

## Page Summary

| Area | Pages | Count |
|---|---|---|
| **Public** | Home, Browse, Component Detail, Seller Profile, About, Terms, Privacy | 7 |
| **Auth** | Sign Up, Sign In (Clerk) | 2 |
| **Buyer** | Downloads, Stars, Reviews | 3 |
| **Seller** | Dashboard, Publish, Edit, Stripe Onboarding | 4 |
| **Admin** | Dashboard | 1 |
| **Total** | | **17 pages** |

---

## Key User Flows

### Buyer Flow
1. Land on Home Page
2. Search or browse on Browse Page
3. View Component Detail Page
4. If free → download directly
5. If paid → Stripe checkout → download unlocked
6. Leave verified review

### Seller Flow
1. Sign up / log in
2. Connect Stripe account (Stripe Onboarding)
3. Publish component (Publish Page)
4. Monitor performance (Seller Dashboard)
5. Respond to reviews/comments (Component Detail Page)
6. Update component as needed (Edit Page)

---

*Document created: June 2026*
