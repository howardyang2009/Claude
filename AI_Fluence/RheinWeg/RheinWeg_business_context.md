# RheinWeg — Business Context Document

*A reusable brief to paste at the start of future conversations so the assistant has full context without re-reading source files. Last updated: 1 July 2026.*

---

## 1. Who

- **Founder:** Liying Zhu. Chinese family, moved to Germany in 2016, now in Oberursel (Taunus), near Frankfurt.
- **Team:** 2 people (founder + wife). Pre-revenue startup.
- **Background:** 20+ years IT experience; strong self-learning habit; comfortable with edge/emerging tech.
- **Company:** RheinWeg (莱茵之路 / "Rhine Road"). Domain: rheinwegde.com. Contact: rheinwegde@gmail.com, +49 160 1168307.
- **Core values:** help others; do no evil; use AI to do more so there's more time to innovate ways to help people.
- **Origin note:** The education work started from a personal question — how to help his own son (Grade 10) and other Chinese students succeed at German universities.

---

## 2. The five threads (current reality)

RheinWeg is presented as one company but actually contains five distinct businesses:

1. **RheinWeg China-bridge B2B** *(chosen focus)* — helping German/European businesses find, verify, and deal with Chinese companies. Three services: (a) find Chinese companies by criteria (€1–2/company); (b) detailed company + credit/due-diligence reports (€20–100/company); (c) representation — first contact, factory visits, negotiation, DE–CN contract translation, signing (2% of contract value). Draws on Chinese corporate databases (e.g. 启信宝/qixin).
2. **Lead-generation / contact-list service** — scraping German business contacts from GelbeSeiten (via a `gelbeseiten-to-xlsx` skill). **Sold as a service to clients.** Treated as a separate cash line, not a funnel into the China business.
3. **AiBlocks** (aiblocks-six.vercel.app) — a marketplace for reusable AI components (prompts, skills, MCP servers, agents, CLAUDE.md configs, hooks); Stripe payouts; 0% fee at launch. *Parked.*
4. **Academic Path / education** — tri-lingual student-success surveys (admin/teacher/student, DE + ZH), letters to German universities, a proposed "Life Mentoring System," and university-visit/immersion trips for Chinese families. *Parked; see reframing note below.*
5. **Yun OS** — an aspirational distributed operating system. No artifact yet. *Parked.*

---

## 3. Strategic decisions reached

- **Focus:** The **China-bridge B2B** is the priority — it's the founder's stated 2-year goal and the thread where his bicultural (Chinese–German) + IT edge is hardest to replicate.
- **Reality check:** Zero paying customers to date. Founder has **never spoken to a target buyer** — the business currently rests on an assumption ("I imagine they want to buy from China"). Fixing this is the top priority.
- **Wedge = verification.** Lead with the due-diligence/verification report, not the full service menu and not representation. It solves an acute, time-bound fear (getting scammed right before wiring money), it's a discrete "prove it once" job, and it builds the trust needed to later win the high-value 2%-representation work.
- **Positioning:** Not "a cheaper report." The differentiator is being a **German-resident, German-speaking, Chinese-native, same-timezone trusted bridge** who can also do the China-side legwork (visits, negotiation). Target an underserved niche: **German-language, German-invoiced, GDPR-clean** service for German Mittelstand importers and German Amazon/e-commerce sellers. Competitors are mostly anonymous, overseas, English-language report mills.
- **Contact-list service:** Keep as a standalone revenue line to fund early months, but it does **not** feed the China-bridge funnel (list buyers ≠ China-sourcing buyers).
- **Education thread:** If revived, reframe the paying customer from *universities* (unlikely to pay) to *Chinese parents/families* (real willingness to pay). Currently parked.
- **AiBlocks & Yun OS:** Off the founder's moat and facing the most competition; parked for now.

---

## 4. Current priority & next actions

1. **Customer discovery — 10–15 conversations** with German importers / Amazon FBA sellers. Goal is to *learn, not sell*. Core questions: *How do you verify a Chinese supplier today? Have you ever been burned? What did it cost?*
2. **Where to find them:** German Amazon FBA / e-commerce seller communities (Facebook groups, Discords, forums); LinkedIn (titles: *Einkauf, Einkäufer, Import, Sourcing, Beschaffung* at SMEs); import/sourcing forums and subreddits; the founder's own network (warm intros beat cold outreach).
3. **First sales artifact:** Build/sharpen a **sample verification report** to show prospects and close the first sale.

---

## 5. Pricing reference

- **RheinWeg's own:** find companies €1–2 each · detail/credit report €20–100 each · representation 2% of contract value.
- **Market comps (verification/due diligence):** CFC ≈ $99/report; CJO Global ≈ $998/company (no on-site visit); SGS / QIMA for factory audits & inspections; DIY route = hiring a Chinese-speaking VA on Upwork to check AIC/GSXT records. RheinWeg's €20–100 is reasonably priced, arguably underpriced.

---

## 6. Open questions (pending decisions)

- Which buyer segment to target first: **German Amazon/e-commerce sellers** vs **traditional import/wholesale SMEs**?
- Is there already a **sample verification report** to show prospects? If not, that's the first artifact to build.

---

## 7. Risks to keep on the radar

- **German cold-email law:** Unsolicited commercial B2B email in Germany generally requires prior consent (UWG §7); scraped address lists are also personal data under GDPR. Bulk outreach to scraped lists carries real legal exposure — verify approach with a lawyer. *(Not legal advice.)*
- **Chinese data sourcing:** Reselling data pulled from Chinese platforms (e.g. qixin) raises terms-of-service questions plus China's cross-border data rules (PIPL / Data Security Law), and GDPR where records include named individuals.
- **Security hygiene:** Project notes currently store live passwords and bot/API tokens in plain text, with one password reused across multiple accounts. Action: rotate credentials, stop password reuse, move secrets into a password manager. *(Do not store real credentials in this or any shared document.)*
