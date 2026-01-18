---
description: Manage the lifecycle of vehicle leads, from ingestion to inspection and tracking.
---

# Vehicle Lead Management Workflow

This workflow guides the AI in managing the `Vehicle-Leads-Tracking.md` file and associated listing folders.

## 1. Lead Ingestion (New Listing)
**Trigger:** User shares a URL or description of a vehicle for sale.

1.  **Extract Data**:
    *   Price, Year, Model, Engine, Transmission, Mileage.
    *   Location (Town/City).
    *   Seller Name.
2.  **Evaluate**:
    *   Compare against **Scorecard Criteria** in `Vehicle-Leads-Tracking.md`.
    *   **Preference Factor**: Favor 1995–1997 models (facelift generation) for better safety/engine.
    *   Assign initial **Rank** and **Score** (High/Medium/Low Match).
3.  **Update Tracker**:
    *   Add row to `Vehicle-Leads-Tracking.md` with Status `🆕 New`.
    *   Format: `| Rank | Status | Year & Model | Price | Spec & Mileage | Score & Notes |`

## 2. Inspection & Contact (Processing Data)
**Trigger:** User provides voice notes, text notes, or photos for a specific vehicle.

1.  **Directory Setup**:
    *   Create folder: `20-Projects/2026-01-16-land-cruiser-80/Listings/[SellerName]-[Locations]-[Model]`.
    *   *Example:* `Chris-McMaster-Melkbosstrand-Land-Cruiser-80`.
2.  **Process Audio (If present)**:
    *   Use `audio-transcriber` skill.
    *   Save transcript and summary to the listing folder.
3.  **Create Documentation**:
    *   Create/Update `Listing-Details.md`: Structured metadata (VIN, Contact info, etc.).
    *   Create `Inspection-Report.md`: Structured assessment of condition (Rust, Mechanical, Drive).
4.  **Update Tracker**:
    *   Change Status to `✅ Inspected` or `📞 Contacted`.
    *   **Sync Feedback**: Update the **Score & Notes** column in the main tracking file with:
        *   Critical findings (e.g., "Rust detected", "Good drive").
        *   Link to the internal `Listing-Details.md`.
        *   User's subjective ranking (e.g., "Better drive than X").

## 3. Maintenance (Re-Ranking)
**Trigger:** User asks to "Update ranks" or after significant updates to inspections.

1.  **Re-Sort Table**:
    *   move **High Match** / **Inspected** items to the top.
    *   Push **Fail** / **Sold** items to the bottom.
2.  **Verify Links**: Ensure all `✅ Inspected` items have valid relative links to their Listing folders.
