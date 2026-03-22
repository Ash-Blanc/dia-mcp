# 📖 DIA MCP Usage Guide & Best Prompts

This guide provides the best ways to utilize the UX Inspo Engine for high-quality design research and inspiration gathering.

---

## 🚀 Best Research Prompts

Use these prompts with your AI assistant (Claude, Cursor, etc.) to trigger complex research workflows.

### 1. Broad Visual Inspiration
**Goal:** Gather diverse visual ideas for a new UI project.
> "I'm designing a **bento-box style dashboard** for a **fintech app**. Use `find_inspo` to find at least 12 references across auto-selected platforms. Focus on dark-mode examples with clean typography."

### 2. Deep Platform Research
**Goal:** Mine a specific high-signal platform like Mobbin for expert patterns.
> "Use `dig_platform` on **Mobbin** to find **onboarding flows** for **SaaS productivity tools**. Look for examples that use progressive disclosure. Limit to 8 high-quality results."

### 3. Competitor Benchmarking
**Goal:** Compare specific pages of multiple competitors side-by-side.
> "I need to compare the **pricing pages** of **Stripe, Linear, and Notion**. Use `compare_uis` to get full-page screenshots of all three. Focus the analysis on their pricing card layouts and feature comparison tables."

### 4. UI/UX Flow Auditing
**Goal:** Document the exact steps and friction points of a real product.
> "Walk through the **signup flow** on **https://linear.app** using `walk_flow`. Document every screen, the specific interactions required to advance, and give me a Senior Researcher's critique of the UX friction."

### 5. Design DNA Extraction
**Goal:** Reverse-engineer the design system tokens of a website.
> "Extract the **Design DNA** from **https://vercel.com**. Give me the color palette, font families, and spacing relationships. Also, index this into the Research Index for future reference."

### 6. Smart Site-Wide Hunting
**Goal:** Explore an entire site selectively for the best patterns.
> "Perform a `site_pattern_hunt` on **https://reark.com**. Smartly find their most unique UI patterns, especially in their documentation and product overview pages. I want to see how they handle complex information hierarchy."

### 7. Expert Color Palette Recommendation
**Goal:** Get curated color palettes with design rationale for a specific niche.
> "I'm building a **meditation and wellness app** that needs to feel **calm, grounding, and accessible**. Use `recommend_colors` to find 5 trending palettes. I want to see the HEX codes and the expert rationale for why these colors work for mental health applications."

### 8. The UX Oracle (Deep Autonomous Research)
**Goal:** Trigger a multi-stage research mission to solve a complex design problem.
> "I need to design a **highly complex data filtering system** for an **enterprise analytics platform**. Use `ux_oracle` with **depth='deep'** to research industry standards, extract the Design DNA of the best examples, and synthesize a report on information density and spatial logic."

---

## 🛠️ Tool-Specific Use Cases

| Tool | Best Use Case | Tip |
| :--- | :--- | :--- |
| `find_inspo` | Early-stage moodboarding | Use descriptive keywords like "glassmorphism", "minimalist", or "high-density". |
| `site_pattern_hunt` | Understanding a site's Design System | Best for "smart" exploration of a site without knowing exact URLs. |
| `walk_flow` | Studying user journey patterns | Use for complex multi-step processes like "KYC verification" or "checkout". |
| `index_flow` | Long-term research memory | Use this to save an entire multi-step flow so you don't have to re-run the agent later. |
| `extract_design_dna` | Building a new token system | Use this to see the proportional relationships (e.g. heading-to-body ratio) of top sites. |
| `recommend_colors` | Visual identity & branding | Combine with `extract_design_dna` to compare your ideas with competitors. |
| `ux_oracle` | End-to-end design research | The 'Master' tool. Use when you have a high-level problem and need a full report. |

---

## 💡 Best Practices for "Better Results"

1. **Be Agentic**: When using TinyFish-based tools (`walk_flow`, `dig_platform`, `index_flow`), give it a persona in your prompt. *Example: "Act as a Senior Interaction Designer..."*
2. **Constrain the Focus**: Use the `focus` or `filters` arguments to prevent the agent from wandering into irrelevant parts of a site.
3. **Use the Index**: Don't just look at inspiration—**index it**. Use `index_pattern` or `index_flow` during your research so that your MCP server builds a unique, private knowledge base of patterns you like.
4. **Keyword Richness**: When searching with `find_inspo`, combine the component name with a style and a niche. *Example: "mobile navigation + minimalist + healthcare".*
5. **Parallelism**: The engine is designed to hit multiple sources in parallel. If you need 20 results, ask for 20—it's often as fast as asking for 5.
