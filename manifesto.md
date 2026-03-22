# dia — the design inspiration agent

**Context augmentation for UI/UX — not code, not docs, not libraries. Screens.**

---

## The Problem

Coding agents now have an incredible context layer. They can read your codebase, navigate your documentation, and understand your library APIs. But they are still **visually illiterate**.

When it comes to the other half of shipping a product — the **design** — agents are guessing. They hallucinate UI patterns the same way they hallucinate deprecated methods: confidently, plausibly, and wrongly. Every day, design-aware engineers lose hours manually hunting for screenshots on Mobbin or Refero, only to lose the context the moment they paste it into a chat window.

**Design context — not generation — is now the bottleneck.** Agents can build anything, but they don't know what "good" looks like right now.

---

## The Thesis

If documentation gives an agent **knowledge**, dia gives an agent **taste**.

dia is a context augmentation layer that makes agents tasteful by providing real-world evidence from the live web. It’s an **MCP server** that hooks directly into the agent's reasoning loop. When your agent needs to know how Linear handles empty states, how Vercel structures navigation, or how the best fintech apps handle KYC flows, it doesn't guess. It asks dia.

And dia answers with **images, structure, and reasoning.**

---

## The Core Principle: Best of the Best

**dia doesn’t find inspiration; it finds the *right* inspiration.**

General search returns noise. dia researches your specific niche first. It identifies the winners—the products that have already solved the friction you're facing—and extracts their design decisions. 

**Example:** Building an onboarding flow for a dev-tool? dia won't show you generic SaaS templates. It will:
1. Identify the most respected products in the dev-tool space (e.g., Resend, Supabase, Convex).
2. Capture their latest screen flows.
3. Deconstruct the patterns that make them work.
4. Return them as a high-signal reference.

---

## The Philosophy

### 1. Inspire, never replicate
dia exists to help agents **understand** the "why" behind a design—the visual hierarchy, the spacing rhythm, and the information density. It is an educator, not a photocopier. Every image is wrapped in **design reasoning** so the agent learns principles, not just pixels.

### 2. Images first, always
Text descriptions of interfaces are lossy. dia’s primary output is high-fidelity **screenshots**. If a tool doesn't return an image, it returns a direct path to one. Speed to visual reference is our North Star.

### 3. The live web is the source of truth
Design trends don't live in training data. They live in shipping products. dia treats the live web as its real-time knowledge base. It bypasses auth walls and navigates complex SPAs to find what is shipping *today*.

### 4. Agent-Native Reasoning
dia doesn't just "show" an image; it explains it in a way an agent can use. 
> **Standard Response:**
> - **What:** [Screenshot of Stripe's Billing Page]
> - **Where:** stripe.com/billing
> - **Why:** Uses a high-contrast side-nav for clarity; information density is managed via progressive disclosure.
> - **DNA:** `Inter`, `Primary: #635bff`, `Spacing: 8px grid`.

### 5. Two Engines, One Surface
dia uses a dual-engine architecture to handle the entire web:
- **Bulk Engine**: For rapid, scalable screenshotting and token extraction from static or structured pages.
- **Interactive Engine**: A background agent that "digs" into gated platforms (Mobbin, Refero, Godly) to handle filters, scrolling, and bot protection.

### 6. Memory that Compounds
Every pattern you save builds your team's local design library. Over time, your dia instance becomes a curated knowledge base specific to your industry and taste. The more you use it, the more "tasteful" your local agent becomes.

---

## What dia Is

- A UI/UX-specific context layer for AI agents.
- A real-time research engine that extracts **Images + Reasoning**.
- A bridge between the design world (Mobbin, Godly) and the coding loop.
- A local, growing index of proven design patterns.

## What dia Is Not

- A component library (like shadcn/ui).
- A screenshot-to-code generator.
- A general-purpose scraper.
- A tool for cloning or copying interfaces.

---

## Core Capabilities

### Prompts
- **`inspo_hunt`** — Kick off a visual research session. dia identifies the winners in your niche and builds an inspiration board.

### Tools
1. **`find_inspo`** — Parallel search across top design platforms.
2. **`screenshot_live_app`** — Instant capture of any URL (Mobile/Desktop).
3. **`dig_platform`** — Navigate gated platforms using natural language goals.
4. **`compare_uis`** — Side-by-side competitive analysis of specific screens.
5. **`extract_design_dna`** — Pull fonts, colors, and spacing systems from any product.
6. **`walk_flow`** — Document multi-step user flows (e.g., "capture the checkout flow").
7. **`index_pattern` / `search_index`** — Build and query your local design MOAT.

---

## The Name

**dia** — *design inspiration agent*.

In Greek, "dia" (διά) means **"through"**—seeing *through* the surface of a design to the principles that make it work.

---

*Inspire, don't copy. Understand, then create.*
