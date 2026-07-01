# AiBlocks — Clerk ↔ Supabase JWT Integration (When & How)

> A "do this later, when you actually need it" note. Captures **why** this
> integration exists, **when** it becomes necessary, and the **how** so future-you
> (or a collaborator) can wire it up safely without weakening security.

---

## TL;DR

- AiBlocks currently talks to Supabase **only through server code** (API routes +
  server components) using the `service_role` key, which bypasses RLS.
- The browser never holds a Supabase client that writes data, so the
  Clerk↔Supabase JWT bridge is **not required today** and is **not blocking launch**.
- Set it up the moment you want the **browser to talk to Supabase directly as a
  signed-in user** (real-time features, client-side reads/writes).
- When you do, wire the JWT properly. **Do NOT** loosen RLS policies to make
  client-side calls work — that's the one genuinely dangerous shortcut.

---

## The two doors into the database

Every request that touches Supabase data comes through one of two doors:

| Door | Key used | Guarded by | Used by AiBlocks today? |
|---|---|---|---|
| **Server** | `service_role` | Your own code checks (RLS bypassed) | **Yes — everything** |
| **Browser** | `anon` | RLS policies only | Not yet |

All current actions — publish, the download paywall, checkout, the Stripe webhook,
every page read — go through the **server door**. Each route resolves the Clerk user,
confirms entitlement, then acts. `createBrowserClient()` exists in the scaffold but
nothing uses it to write yet.

---

## What the JWT integration actually fixes

RLS policies identify the user via `auth.jwt() ->> 'sub'`, expecting the **Clerk user
id**. But Supabase doesn't know anything about Clerk — they're separate services. So
when a browser hits Supabase with only the `anon` key, `auth.jwt()` is null and every
user-scoped policy **denies**.

Result: the browser door is currently locked to **public reads only** (policies written
`using (true)`, e.g. reading published components). No *authenticated* client-side
action works.

The JWT integration is the bridge: Clerk mints a token Supabase trusts, carrying the
Clerk user id as the `sub` claim. Once configured, `auth.jwt() ->> 'sub'` resolves, and
the existing RLS policies "wake up" — a signed-in user can safely read their own
purchases, write their own star, etc., **directly from the browser**, scoped by RLS to
their own rows.

---

## When you need it — and when you don't

**You DON'T need it while** every authenticated action flows through a server route
(today's architecture). Example: the star button POSTs to `/api/components/[id]/star`,
which uses the service role — the browser never writes to Supabase directly.

**You DO need it when** you want the browser to act as a logged-in user against
Supabase directly, e.g.:
- Real-time subscriptions (live comments, live star/download counts)
- Optimistic client-side reads/writes that skip a round-trip through your API
- Any direct `createBrowserClient()` query that depends on "who am I"

---

## Is this "more secure"? Be precise.

Setting up the JWT does **not** make the current app more secure on its own — the
server routes are already the enforcement layer and they're sound.

What it buys you is **defense in depth**: RLS becomes a real second line of defense
instead of a locked door you route around. The genuine risk it addresses is *future
and architectural* — the day someone adds a quick client-side Supabase call without
going through an API route, properly-wired RLS keeps that shortcut safe by default.

The dangerous middle path to avoid: leaving RLS enabled but **loosening policies** so
the browser door works without auth. That's how marketplaces accidentally expose data.
If you need the browser door, do the JWT integration — don't weaken the policies.

---

## How to set it up (when the time comes)

> ~20 minutes. Steps are written from memory of the integration shape; check the
> current Clerk + Supabase docs for exact UI labels, as dashboards change.

### 1. Create a JWT template / signing config in Clerk
- In the Clerk dashboard, create a JWT template intended for Supabase.
- The token must expose the Clerk user id as the `sub` claim (it does by default).
- Clerk provides the signing details (a JWKS endpoint / issuer) you'll give Supabase.

### 2. Tell Supabase to trust Clerk's tokens
- In Supabase Auth settings, configure the **third-party auth / external JWT** option
  so Supabase accepts tokens issued by your Clerk instance (issuer + JWKS URL).
- This makes `auth.jwt()` populated when a request arrives with a Clerk-issued token.

### 3. Attach the token on the browser client
- Update `lib/supabase/client.ts` so `createBrowserClient()` fetches the Clerk token
  and sends it as the `Authorization: Bearer <token>` header on Supabase requests.
- Sketch (adapt to current Clerk API):

```ts
"use client";
import { createClient } from "@supabase/supabase-js";
import { useSession } from "@clerk/nextjs";

export function useSupabaseBrowser() {
  const { session } = useSession();
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      global: {
        fetch: async (url, options = {}) => {
          const token = await session?.getToken(); // Clerk token for Supabase
          const headers = new Headers(options.headers);
          if (token) headers.set("Authorization", `Bearer ${token}`);
          return fetch(url, { ...options, headers });
        },
      },
    }
  );
}
```

### 4. Verify RLS actually engages
- Signed in, do a client-side read of your own `purchases` — it should succeed.
- Signed out (or as another user), the same read should return **nothing**.
- If a signed-in client-side write is denied, check that the token's `sub` matches a
  `profiles.clerk_user_id` and that the relevant policy references it correctly.

### 5. Keep the server door as-is
- Privileged, security-critical actions (download paywall, webhook, purchase writes)
  should **stay** on the server with the service role. The JWT/browser path is for
  user-scoped convenience reads/writes, not for the money path.

---

## Decision shortcut

- Shipping V1, everything server-routed → **skip this for now.**
- Reaching for real-time or direct client-side authed Supabase calls → **do this,
  properly**, before writing those calls.
- Tempted to loosen RLS so the browser "just works" → **stop**; do the JWT instead.

---

*Document created: June 2026. Project: AiBlocks.*
*Companion to: AiBlocks_Schema.sql, 0002_rls.sql, AiBlocks_Vercel_Deployment_Checklist.md*
