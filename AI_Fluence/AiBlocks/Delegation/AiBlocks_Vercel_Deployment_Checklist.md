# AiBlocks — Vercel Deployment Checklist

> An ordered, do-this-then-that guide for taking AiBlocks live on Vercel.
> Stay in **Stripe test mode** for the whole of this checklist — it proves the
> production *path* (real internet, real webhook) without taking real money.
> Going fully live (real cards) is a separate, deliberate switch covered at the end.

---

## The one ordering trap to remember

You cannot register the Stripe webhook until the app is deployed and has a URL,
but the app needs *most* of its env vars to deploy usefully. So the sequence is:

1. Deploy with all env vars **except** the production webhook secret.
2. Grab the live Vercel URL.
3. Register the webhook in Stripe → get its signing secret.
4. Add that secret to Vercel → **redeploy once** so it takes effect.
5. Run one test purchase against the live URL.

Work top to bottom and this resolves itself.

---

## Phase 1 — Pre-deploy sanity (local)

- [x] App runs locally with `npm run dev` and a full test purchase unlocks a download.
- [x] `.env.local` is **not** committed (only `.env.example` is in the repo).
- [x] Latest code is pushed to `github.com/howardyang2009/aiblocks` (`main` branch).
- [x] `npm run build` succeeds locally (catches issues Vercel would hit at build time).

> Note: `.env.local` is gitignored on purpose, so Vercel sees **none** of your keys
> until you add them in Phase 3. A clean build that fails every Stripe/Supabase/Clerk
> call in production is almost always a missing env var.

---

## Phase 2 — Connect the repo to Vercel

- [x] Sign in to https://vercel.com with GitHub.
- [x] **Add New… → Project**, import the `aiblocks` repo.
- [x] Framework preset auto-detects **Next.js** — leave defaults.
- [x] **Do not deploy yet** — add environment variables first (Phase 3), or let the
      first build fail and add them right after. Either way, env vars must be set
      before the app will actually work.

---

## Phase 3 — Environment variables (Vercel → Settings → Environment Variables)

Add every key the app needs. Use your **test-mode** Stripe keys for now.
Apply them to the **Production** environment (and Preview, if you want PR previews to work).

### Supabase
- [x] `NEXT_PUBLIC_SUPABASE_URL` = `https://mvuzsjhqqggcccydflkv.supabase.co`
- [x] `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `eyJ…` (anon / public key)
- [x] `SUPABASE_SERVICE_ROLE_KEY` = `eyJ…` (**secret** — server only, bypasses RLS)
- [x] `SUPABASE_ZIP_BUCKET` = `component-zips`

### Clerk
- [x] `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` = `pk_test_…` (or `pk_live_…` at real launch)
- [x] `CLERK_SECRET_KEY` = `sk_test_…` (**secret**)
- [x] `NEXT_PUBLIC_CLERK_SIGN_IN_URL` = `/sign-in`
- [x] `NEXT_PUBLIC_CLERK_SIGN_UP_URL` = `/sign-up`

### Stripe
- [x] `STRIPE_SECRET_KEY` = `sk_test_…` (**secret**)
- [x] `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` = `pk_test_…`
- [x] `STRIPE_WEBHOOK_SECRET` = *(leave blank or placeholder for now — set in Phase 5)*

### App
- [x] `NEXT_PUBLIC_APP_URL` = `https://aiblocks-six.vercel.app/`
      (your real Vercel URL — **not** `localhost`. Checkout builds the Stripe
      success/cancel redirects from this; localhost here bounces buyers to localhost.)

> Secrets (`SUPABASE_SERVICE_ROLE_KEY`, `CLERK_SECRET_KEY`, `STRIPE_SECRET_KEY`,
> `STRIPE_WEBHOOK_SECRET`) must **never** be prefixed `NEXT_PUBLIC_`. Anything
> `NEXT_PUBLIC_` is shipped to the browser.

---

## Phase 4 — First deploy

- [x] Trigger a deploy (push to `main`, or **Deploy** in the Vercel dashboard).
- [x] Build succeeds.
- [x] Visit `https://aiblocks-six.vercel.app/` — home page loads.
- [x] Sign in works (Clerk). If Clerk shows a domain error, see "Clerk production"
      note below.
- [x] Browse shows your real published components (confirms Supabase reads work).

---

## Phase 5 — Register the production webhook (Stripe)

- [x] Stripe dashboard (test mode) → **Developers → Webhooks → Add endpoint**.
- [x] Endpoint URL: `https://aiblocks-six.vercel.app/api/webhooks/stripe`
- [x] Events to send: select **`checkout.session.completed`**
      (optionally also `checkout.session.async_payment_succeeded`).
- [x] Save → copy the endpoint's **Signing secret** (`whsec_…`).
      This is a **different** secret from your local `stripe listen` one.
- [x] In Vercel → Environment Variables, set `STRIPE_WEBHOOK_SECRET` = that `whsec_…`.
- [x] **Redeploy** (env changes only apply to the next deployment, not retroactively).

---

## Phase 6 — Verify the full loop in production

- [x] As a seller: `/dashboard/seller/stripe` → complete Express onboarding (test data).
- [x] Publish a component with a price.
- [x] As a buyer: **Buy to download** → Stripe Checkout → card `4242 4242 4242 4242`,
      any future expiry, any CVC.
- [x] Stripe dashboard → Webhooks → your endpoint shows a successful `200` delivery
      for `checkout.session.completed`.
- [x] Supabase: the `purchases` row reads `succeeded`, and a `downloads` row now exists.
- [x] The download unlocks and the zip downloads via a signed URL.

If all boxes are checked, AiBlocks works over the real internet path.

---

## Notes you'll likely need

### Clerk production instance
The `pk_test_/sk_test_` Clerk keys work on `localhost` and Vercel preview URLs, but for
a real custom domain you create a **production instance** in Clerk, register your own
OAuth apps (Google/Microsoft/etc.), add your domain, and use `pk_live_/sk_live_` keys.
Fine to launch on the `*.vercel.app` URL with test keys first; switch when you add a domain.

### Webhook signature = raw body
The webhook route verifies Stripe's signature against the **raw** request body
(it uses `req.text()`, not JSON parsing). This is already correct — don't change it,
or verification fails with a 400 and purchases stop unlocking.

### Auto-deploys
Vercel redeploys on every push to `main`, with preview deployments per pull request.
After changing any env var, redeploy for it to take effect.

---

## Going fully live (later — not now)

Test mode does **not** carry over to live automatically. When you're ready for real money:

- [x] Activate your Stripe account (business details, bank for payouts).
- [x] Swap Vercel env to **live** keys: `sk_live_…`, `pk_live_…`.
- [x] Create a **separate live-mode** webhook endpoint (live mode has its own
      endpoints and its own signing secret) → update `STRIPE_WEBHOOK_SECRET`.
- [x] Sellers re-onboard through **live** Connect.
- [ ] Switch Clerk to its production instance + live keys.
- [x] Replace placeholder Terms / Privacy with reviewed legal copy (Human-Led).
- [x] Redeploy and run one real low-value purchase to confirm payouts route correctly.

---

*Document created: June 2026. Project: AiBlocks.*
