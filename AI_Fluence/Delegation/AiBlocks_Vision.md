# AiBlocks — Product Vision Document

> A universal marketplace for reusable AI components — cross-ecosystem, community-driven, with optional paid downloads.

---

## What is AiBlocks?

AiBlocks is an open marketplace where anyone can publish and download reusable AI building blocks — prompts, skills, agents, MCP servers, CLAUDE.md configs, hooks, and more. Think of it as **npm for AI components**, designed for builders across all major AI ecosystems.

---

## Component Types Supported

- Use case prompts
- Reusable skills
- Reusable agents
- Reusable hooks
- Reusable CLAUDE.md configurations
- Reusable MCP servers
- Any other AI building block

---

## Core Decisions

### 🌐 Ecosystem
- **Multi-AI** — supports components for any AI platform
- Includes: Claude, ChatGPT, Gemini, Deepseek, and others
- Components tagged by ecosystem so buyers know compatibility

### 📤 Submission
- **Open** — anyone can publish a component
- No manual curation or gating by the platform
- Quality is determined by the community

### ⭐ Quality Control
- Community-driven signals only:
  - **Star count** — community endorsement
  - **Download count** — popularity and trust
  - **Verified buyer reviews** — written reviews with star ratings
  - **Open comments** — anyone can ask questions or comment
- Sellers can reply to reviews and comments
- Lightweight abuse reporting (v2)

### 💳 Monetization
- Sellers set their own price (free or paid)
- Payments via **Stripe Connect** — money flows directly to seller
- **0% platform fee** at launch (to attract sellers)
- Hard paywall — buyers must pay before downloading a paid component
- Stripe's standard processing fee applies (~2.9% + 30¢)

### 🔍 Discovery
- **Text search bar** — searches title and description
- **Clickable tag filters** — free-form tags with autocomplete suggestions
- Tags are set by sellers (free-form, not predefined)
- Autocomplete helps naturally converge the tag taxonomy

### 📄 Component Pages
- **Markdown README** — separate field on submission form, rendered on component page
- **Metadata** — author, ecosystem, price, downloads, stars, tags
- **Reviews section** — verified buyer reviews + open comments
- **Download / Buy button**

### 📦 File Format
- Sellers upload a single **zip file**
- Maximum file size: **10MB**
- README is a separate markdown field (not inside the zip)

### 🔐 Authentication
- **OAuth providers:** Google, Microsoft, Facebook, GitHub
- **Email/password** registration also supported
- Auth provider: **Clerk**

### 🔄 Versioning
- **No versioning** — always latest
- Sellers update their component in place
- Sellers can maintain a changelog in their markdown README

### 👤 Seller Profiles
Public profile page per seller, including:
- Avatar, display name, bio
- Links (GitHub, Twitter, personal site)
- Joined date
- **Stats:** total components, total downloads, total stars
- **Component grid:** all published components, sortable by stars / downloads / newest
- Future: Verified badge, Top Seller badge

---

## Key User Flows

### Seller Flow
1. Sign up / log in
2. Create component listing (name, description, markdown README, tags, ecosystem, price)
3. Upload zip file (max 10MB)
4. Connect Stripe account
5. Publish component
6. Respond to reviews and comments
7. Update component in place as needed

### Buyer Flow
1. Browse or search AiBlocks
2. Filter by tags and/or ecosystem
3. View component detail page (README, reviews, metadata)
4. If free → download directly
5. If paid → complete Stripe checkout → download unlocked
6. Leave a verified review after purchase

---

## What AiBlocks is NOT (v1 Scope)

- ❌ No versioning system
- ❌ No platform fee (yet)
- ❌ No manual curation or approval process
- ❌ No AI-powered semantic search (v2 candidate)
- ❌ No abuse/fraud system (v2 candidate)

---

## Summary

| Dimension | Decision |
|---|---|
| **Name** | AiBlocks |
| **Ecosystem** | Multi-AI (Claude, GPT, Gemini, etc.) |
| **Submission** | Open — anyone can publish |
| **Quality control** | Community signals (stars, downloads, reviews) |
| **Monetization** | Stripe Connect, direct to seller, 0% fee now |
| **Download gate** | Hard paywall — must pay before download |
| **Component page** | Markdown README + metadata + tags |
| **Search** | Text search + clickable free-form tags with autocomplete |
| **Auth** | OAuth (Google, Microsoft, Facebook, GitHub) + Email/Password |
| **Auth provider** | Clerk |
| **Versioning** | No versioning — always latest |
| **File format** | Zip, max 10MB |
| **README** | Separate markdown field on submission form |
| **Reviews** | Verified buyer reviews (star + text) + open comments, seller can reply |
| **Seller profiles** | Public page — bio, stats, all components |

---

*Document created: June 2026*