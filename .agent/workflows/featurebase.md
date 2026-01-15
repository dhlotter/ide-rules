---
description: "Slash‑command workflow for /featurebase – produces an internal technical recap and a user‑facing update"
---

# **/featurebase Workflow**

When the agent receives the slash command **`/featurebase`**, it should output **two clearly separated sections**:

---

## 1️⃣ Internal Ticket – Detailed Technical Recap

*Purpose:* Provide the engineering team with a complete record of the work.

**Content to include (in this order):**

1. **Issue / Problem** – Brief description of the symptom (e.g., "The application crashed when clicking the 'Export' button on the results page").
2. **Root Cause** – What caused the issue (e.g., "The export handler was attempting to access a null reference when no results were selected").
3. **Fix Implemented** – Summary of the technical changes (e.g., "Added a null check to the export handler and disabled the 'Export' button when no items are selected").
4. **Verification / Testing** – Steps taken to confirm the fix works (e.g., "Verified that the 'Export' button is now disabled by default and that clicking it with selections works as expected; verified no crashes occur").
5. **Outcome / Metrics** – Quantitative results if applicable (e.g., "Resolved 100% of reported crashes related to exports").

*Formatting:* Use markdown headings (`##`) and bullet points for readability. No personal or confidential user data should appear.

---

## 2️⃣ Public Update – Non‑Technical Summary

*Purpose:* Communicate the improvement to end‑users in plain language.

**Content to include (in this order):**

1. **What the user saw before** – Simple statement of the problem (e.g., "Clicking the export button could sometimes cause the app to close unexpectedly").
2. **What we did** – Plain description of the fix (e.g., "We fixed a bug in the export system and updated the button to only be clickable when you have items selected").
3. **Result for the user** – Clear benefit (e.g., "Exporting your data is now more reliable and stable").
4. **Any next steps** – If applicable (e.g., "No action is required; the fix is live now").

*Formatting:* Use short paragraphs or bullet points, friendly tone, no technical jargon.

---

### How the Agent Should Execute the Workflow

1. Detect the slash command `/featurebase`.
2. Gather relevant details from the task context and history.
3. Render the two sections exactly as described, separating them with a clear divider (e.g., `---`).
4. Return the composed markdown to the user.
