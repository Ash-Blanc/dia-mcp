# MANIFESTO.md

# dia — the design inspiration agent

**Context augmentation for UI/UX — not code, not docs, not libraries. Screens.**

---

## The Problem

Coding agents got their context layer. Nia solved it for codebases and
documentation. Context7 solved it for library docs. But nobody solved it
for the other half of shipping product: **the design**.

Every day, designers and design-aware engineers do the same ritual. Open
Mobbin. Open Dribbble. Open Refero. Screenshot things. Paste them into
Figma or a chat window. Describe what they saw. Lose the reference. Do
it again tomorrow. There is no persistent, searchable, agent-accessible
layer for visual design context.

AI agents can now generate entire frontends. What they cannot do is
**taste**. They have no sense of what good looks like right now, what
patterns are shipping in real products today, what the best teams chose
and why. They hallucinate UI the same way they hallucinate API methods —
confidently, plausibly, wrongly.

**Design context — not generation — is now the bottleneck.**

---

## The Thesis

If Nia is the context augmentation layer that makes coding agents
reliable by giving them access to the right documentation and code,
**dia is the context augmentation layer that makes design-aware agents
tasteful** by giving them access to the right screens, flows, patterns,
and design reasoning.

dia is an MCP server. It plugs into Cursor, Claude Desktop, VS Code,
or anything that speaks MCP. When your agent needs to know what a great
onboarding flow looks like, what the best SaaS pricing pages are doing,
how Linear handles empty states, or what design tokens Vercel uses —
it asks dia. And dia answers with **images, structure, and reasoning**.

Not with opinions. With evidence from the live web.

---

## The Core Principle: Best of the Best

**dia doesn't just find inspiration — it finds the *right* inspiration.**

When you ask for UI/UX inspiration, dia first identifies the most
successful, most respected products in your specific niche. It doesn't
pull random screenshots from random apps. It researches the market,
finds the winners, and draws from their design decisions.

**Example:** If you're building a landing page for an MCP project, dia
won't show you generic SaaS templates. It will:
1. Identify the most successful MCP products (trynia.ai, morphllm.com, etc.)
2. Screenshot their landing pages
3. Extract the patterns that make them work
4. Return those as your reference — because they're proven in *your* space

**This is the difference between "inspiration" and "relevant inspiration."**
The best onboarding flow for a fintech app isn't the best onboarding flow
for a developer tool. dia knows the difference because it researches
your niche first.

---

## The Philosophy

### 1. Inspire, never replicate

This is the cardinal rule. dia exists to make the agent (and the human
behind it) **understand** what makes a design work — the visual
hierarchy, the spacing rhythm, the information density, the interaction
pattern. It does not exist to photocopy someone else's UI.

Every response wraps images in **design reasoning**: why this works,
what principle it demonstrates, what pattern it belongs to. The agent
learns to think in principles, not pixels.

### 2. Images first, always

Design is visual. Text descriptions of interfaces are lossy. dia's
primary output is **screenshots** — of real shipped products, of
curated galleries, of live apps captured in the moment. If a tool
doesn't return an image, it should return a URL to one. Speed to
visual reference is the metric that matters.

### 3. The live web is the source of truth

Design trends don't live in training data. They live on Mobbin, Refero,
Dribbble, Godly, and in the actual products people use today. dia
treats the live web as its knowledge base. It searches it, navigates
it, screenshots it, and extracts structure from it — in real time.

### 4. Depth over breadth in a niche

dia is not a general-purpose web research tool. It is not a scraper.
It is a **deep, opinionated** system that knows exactly where to look
for UI/UX inspiration, how to navigate those sources (including ones
with complex SPAs and filter UIs), and how to extract signal from them.
It knows that Mobbin is king for mobile screens, that Refero has the
best component-level tagging, that Godly captures motion design, that
Behance has the case studies with the "why."

The niche is not "UI/UX in general." The niche is: **finding the
best reference from the most successful products in your exact space,
faster than any human could.**

### 5. Two engines, one surface

dia is powered by two complementary backends:

- **Firecrawl** — the bulk engine. Search the web, screenshot any URL,
  batch-capture pages, extract design tokens and branding, crawl entire
  design systems. Fast, parallel, scalable. Handles the static and the
  structured.

- **TinyFish** — the agent engine. Navigate dynamic SPAs like Mobbin
  and Refero using natural-language goals. Click through filters, scroll
  galleries, handle auth walls and bot protection. Handles the
  interactive and the guarded.

The split is deliberate. Firecrawl for what can be fetched. TinyFish
for what must be *navigated*. The user never thinks about which engine
runs — they ask for inspiration and get it.

### 6. Memory that compounds

dia doesn't just fetch — it **indexes**. Every pattern you save builds
a local knowledge base. Over time, your dia instance becomes a curated
design library specific to your taste, your industry, your product.
The more you use it, the more context it has. The more context it has,
the better it gets.

### 7. The agent serves the designer

dia is not a replacement for design judgment. It is a **research
assistant** that eliminates the busywork of finding references so the
designer (or design-literate engineer) can spend their time on the
hard part: deciding what to build and why. The agent finds. The human
decides.

---

## What dia Is

- An MCP server built with FastMCP (Python)
- A UI/UX-specific context layer for AI agents
- A real-time design research engine backed by Firecrawl + TinyFish
- A local, growing index of design patterns and references
- A tool that returns **images + reasoning**, not templates
- A system that finds inspiration from **the most successful products in your niche**

## What dia Is Not

- A design system generator
- A UI component library
- A screenshot-to-code tool
- A way to clone someone's interface
- A general web scraper that happens to hit design sites
- A random screenshot aggregator

---

## The Name

**dia** — *design inspiration agent*.

Three letters. Lowercase. In Greek, "dia" (διά) means "through" —
as in, seeing *through* the surface of a design to the principles
underneath. That's the whole point.

---

## The Stack

| Layer          | Technology             | Role                                    |
|----------------|------------------------|-----------------------------------------|
| Protocol       | MCP                    | Universal agent interface               |
| Framework      | FastMCP (Python 3.13+) | Server scaffold, tool registration      |
| Bulk engine    | Firecrawl API          | Search, scrape, screenshot, branding    |
| Agent engine   | TinyFish API           | Navigate dynamic platforms, walk flows  |
| Persistence    | SQLite (aiosqlite)     | Local pattern index, growing over time  |
| Package mgmt   | uv                     | Fast, reproducible Python environments  |
| Quality        | ruff, pyright, pytest  | Linting, formatting, type-safety, tests |

---

## Core Capabilities (Tools & Prompts)

### Prompts
- **`inspo_hunt`** — Kick off a full visual research session. The agent receives a project description, identifies the most successful products in that niche, and compiles an inspiration board from those winners.

### Tools
1. **`find_inspo`** — Search multiple curated inspiration platforms in parallel.
   Return the best screens for any design need as images alongside design guidance.

2. **`screenshot_live_app`** — Capture any live product's UI. Mobile or desktop.
   Full page or viewport. Tries to dismiss popups automatically.

3. **`dig_platform`** — Deploy an AI agent into gated/complex platforms like Mobbin, Refero, or Godly to
   navigate filters, scroll results, and extract structured data
   that can't be simply scraped.

4. **`compare_uis`** — Screenshot multiple competitors side by side for
   the same screen type. See how different products solve the same
   problem differently.

5. **`extract_design_dna`** — Pull the design DNA from any site: colors, fonts,
   typography scale, spacing, button styles. Understand the system
   behind the surface.

6. **`walk_flow`** — Have an AI agent click through a real multi-step flow
   (onboarding, checkout, settings) and document every screen.

7. **`index_pattern`** — Save any pattern to your local (`UX_INSPO_INDEX_DIR`) research database with
   category, tags, screenshots, and notes. Build your library.

8. **`search_index`** — Query your accumulated local index by category, tag, or
   free text. Your past research is always one tool call away.

---

## The Standard

When dia returns a design reference, it always answers three questions:

1. **What** — the image, the screenshot, the visual evidence
2. **Where** — the source, the app, the platform it came from
3. **Why** — the design principle it demonstrates, the pattern it
   belongs to, the reason it works

If a response is missing any of the three, it's incomplete.

---

*Inspire, don't copy. Understand, then create.*
