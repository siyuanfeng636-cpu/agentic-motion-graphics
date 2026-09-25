# Motion Graphics Prompt Library & Archetype Templates

This reference contains production-tested prompt templates and structural guidelines for Claude Opus 5.5 and coding agents to generate 5 major categories of commercial motion graphics videos.

---

## 1. SaaS Product Launch Video

### 🎯 Intent & Characteristics
* **Audience**: B2B buyers, indie hackers, investors, tech Twitter/X.
* **Duration**: 30 - 60 seconds.
* **Aspect Ratio**: 16:9 (`1920x1080`) or 1:1 (`1080x1080`).
* **Rhythm**: 120 BPM tempo grid. Cuts happen exactly every 2 or 4 beats (1.0s or 2.0s).
* **Visual Style**: Sleek dark/light mode UI, subtle glassmorphism, perspective tilted browser frames, smooth cursor clicks, animated counters.

### 📝 Master Prompt Template
```text
Role: You are an elite Motion Graphics Director and Creative Frontend Engineer.
Task: Create an official 45-second SaaS product launch video for "{PRODUCT_NAME}".

Source Material:
- Website URL: {WEBSITE_URL}
- Core Value Prop: {VALUE_PROP}
- Target Audience: {AUDIENCE}

Strict Requirements:
1. Asset Fetching: Inspect {WEBSITE_URL}, download authentic SVG logos, high-res UI screenshots, color palettes, and typography. Do not hallucinate fake UI elements if authentic assets are accessible.
2. Narrative Arc:
   - 00:00 - 00:05 (Hook): The burning problem / current broken workflow.
   - 00:05 - 00:15 (Reveal): Introduce {PRODUCT_NAME} with an explosive entrance & hero UI showcase.
   - 00:15 - 00:35 (Features): 3 rapid-fire killer features shown with dynamic perspective zooms and active cursor interactions.
   - 00:35 - 00:45 (Social Proof & CTA): Impressive traction metric + crisp Call-To-Action ("Get started free").
3. Musical Sync: All cuts, zooms, and card flips MUST snap to a 120 BPM grid (0.5s beat, 2.0s measure).
4. Deliverable: Full project code in `~/Projects/videos/{PRODUCT_SLUG}/` with `scripts/script.json`, `index.html` (GSAP), synced audio, and rendered MP4 via HyperFrames.
```

---

## 2. Article / Paper / SOP Explainer Cartoon

### 🎯 Intent & Characteristics
* **Audience**: General tech audience, internal engineering teams, students.
* **Duration**: 90 seconds - 3.5 minutes.
* **Aspect Ratio**: 16:9 (`1920x1080`).
* **Visual Style**: Clean flat vector illustration (hand-drawn SVG elements), friendly robot/mascot narrator, kinetic conceptual diagrams.

### 📝 Master Prompt Template
```text
Role: You are an expert Science & Technology Explainer Animator.
Task: Convert the technical paper / essay "{TITLE}" into an engaging, accessible animated video explainer.

Source Material:
- Source Text/Paper: {SOURCE_DOCUMENT_OR_URL}
- Tone: Engaging, humorous, clear, intellectually honest.

Strict Requirements:
1. Core Conceptual Metaphor: Invent a strong, unifying visual metaphor that makes the abstract concepts tangible (e.g., race cars with a safety pace car for AI regulation, a multi-gear watch mechanism for distributed consensus).
2. Character & Scenery: Draw distinct SVG vector characters (e.g. friendly robots, animated vehicles, interactive nodes). Keep styling consistent across all scenes.
3. Scene Breakdown (`scripts/script.json`):
   - Hook: Why this matters right now.
   - Context: The underlying bottleneck or historical status quo.
   - Mechanism: How the breakthrough works step-by-step.
   - Real-world Impact: What this unlocks for the future.
4. Audio & Narration: Generate warm, clear voiceover narration. Ensure word-level timestamp alignment so SVG character mouth/movement and captions synchronize with spoken audio.
```

---

## 3. Longform to Shortform Viral Video

### 🎯 Intent & Characteristics
* **Audience**: TikTok, Instagram Reels, YouTube Shorts, X vertical video.
* **Duration**: 30 - 75 seconds.
* **Aspect Ratio**: 9:16 (`1080x1920` Vertical).
* **Visual Style**: Large bold kinetic captions (word-by-word active highlight), floating 3D emojis/icons, quick visual transitions every 1.5 - 2.5 seconds, strong color contrast.

### 📝 Master Prompt Template
```text
Role: You are a Viral Short-Form Video Producer specializing in tech and business content (Greg Isenberg / Alex Hormozi aesthetic).
Task: Ingest the transcript of this longform video and transform it into a viral 60-second 9:16 vertical short.

Input:
- Longform Transcript / Video URL: {TRANSCRIPT_OR_URL}
- Target Style: High-retention vertical kinetic explainer.

Strict Requirements:
1. The 3-Second Hook: Rewrite the opening into an irresistible pattern-interrupt hook (e.g., "This new AI model just changed everything, and almost nobody noticed...").
2. Core Structure: Deliver "3 to 5 actionable takeaways" with zero fluff. Every single sentence must provide value or intrigue.
3. Visual Layout:
   - Safe Area: Center all critical UI/text within the middle 60% vertical safe zone.
   - Kinetic Typography: Large, high-impact font (Inter/Cabinet Grotesk/Montserrat 700+), rendering word-level karaoke-style highlight boxes.
   - Dynamic Accents: Animated badges, stat pills, floating badges, and high-frequency sound effects (clicks, whooshes).
```

---

## 4. Personalized Commercial Proposal Video

### 🎯 Intent & Characteristics
* **Audience**: Prospective high-ticket clients, enterprise buyers.
* **Duration**: 90 - 150 seconds.
* **Aspect Ratio**: 16:9 (`1920x1080`).
* **Visual Style**: Clean agency aesthetic, client brand colors, personalized mascot/avatar, interactive milestone timeline.

### 📝 Master Prompt Template
```text
Role: You are an Executive Creative Director and Solutions Architect.
Task: Convert this formal commercial proposal into an impressive, personalized animated video walkthrough.

Input:
- Client Proposal Document: {PROPOSAL_DOC}
- Client Name & Brand: {CLIENT_INFO}

Strict Requirements:
1. Personalization: Include client's logo, brand palette, and name in the greeting scene.
2. Animated Mascot: Create an animated guide mascot (e.g., Pip the Helper Robot) wearing a badge with the client's initial.
3. Content Walkthrough:
   - Diagnosis: Summarize client's current pain points and missed opportunities.
   - Roadmap: Visualize Phase 1, Phase 2, and Phase 3 deliverables on an animated progress track.
   - ROI & Outcomes: Dynamic counters displaying expected revenue lift or time saved.
4. Export: Render both full-fidelity MP4 (1080p) and an optimized email-ready version under 10MB.
```

---

## 5. Dynamic Presentation Conversion

### 🎯 Intent & Characteristics
* **Audience**: Keynote audiences, webinars, VSL (Video Sales Letter).
* **Duration**: Interactive slide deck or continuous video.
* **Visual Style**: Presentation slides with living, breathing dynamic components (pulsing nodes, floating charts, animated gradient mesh).

### 📝 Master Prompt Template
```text
Role: You are a Creative Technologist specializing in interactive presentations.
Task: Upgrade this static HTML/Markdown presentation deck into a dynamic motion presentation.

Input:
- Static Deck File: {SLIDES_FILE}

Strict Requirements:
1. Preserve Original Content: Every slide's exact text, structure, and points must remain intact.
2. Dynamic Upgrades:
   - Transform bullet points into cascading animated cards.
   - Transform static diagrams into interactive SVG node networks with pulsing data packets.
   - Animate headline typography with smooth stagger reveals.
3. Controls: Include keyboard shortcuts for live presentation:
   - `D`: Toggle dynamic / static view
   - `R`: Replay current slide animation
   - `F`: Fullscreen toggle
   - Left/Right arrows: Slide navigation
```
