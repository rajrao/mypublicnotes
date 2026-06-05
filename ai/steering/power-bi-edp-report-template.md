---
inclusion: manual
---

# Power BI EDP Report Template Skill

Scaffold a branded Power BI report following the Enterprise Data Platform (EDP) template standard. This includes page layout, branded images, background patterns, theme, and standard visuals placement.

## Report Structure

The template report has 5 pages:

| Order | Page Name | Visibility | Purpose |
|-------|-----------|------------|---------|
| 1 | Landing Page | Visible | Dashboard home with Dataset Info table and branding |
| 2 | EDP Template | Visible | Main content page with sample visuals layout |
| 3 | Image Assets | Hidden | Stores reference images for the report |
| 4 | Version | Hidden | Version tracking page |
| 5 | Instructions | Hidden | Developer instructions (hidden from viewers) |

## Report-Level Settings

```json
{
  "themeCollection": {
    "baseTheme": { "name": "CY23SU04", "type": "SharedResources" },
    "customTheme": { "name": "Hitachi<id>.json", "type": "RegisteredResources" }
  },
  "settings": {
    "useStylableVisualContainerHeader": true,
    "exportDataMode": "AllowSummarized",
    "defaultDrillFilterOtherVisuals": true,
    "allowChangeFilterTypes": true,
    "useEnhancedTooltips": false,
    "useDefaultAggregateDisplayName": true
  }
}
```

## Page Dimensions

All pages: **1280×720**, displayOption: `FitToPage`

## Landing Page Layout

| Visual | Type | Position (x, y) | Size (w×h) | Content |
|--------|------|-----------------|------------|---------|
| Dataset Info Table | tableEx | 418, 173 | 363×280 | Columns: Data, DateTime. DateTime has webURL conditional formatting using Convertor URL column. Totals disabled. |
| EDP Logo | image | 1117, 54 | 149×63 | EDP_Logo_Final_Transparent. Links to SharePoint EDP site. |
| Hitachi Logo | image | 1103, 0 | 177×54 | Hitachi-InspireTheNext logo. Top-right corner. |

## EDP Template Page Layout

### Page Background
- Image: `Vector-Pattern_White_RGB_sm.png`
- Scaling: Normal
- Transparency: 35%

### Outspace Pane
- Width: 182px

### Visual Placement

| Visual | Type | Position (x, y) | Size (w×h) | Data Binding |
|--------|------|-----------------|------------|--------------|
| Donut Chart | donutChart | 0, 0 | 327×301 | Category: Calendar[Fiscal Year Quarter], Value: Count of Calendar[Date]. Sorted descending by value. |
| Column Chart | columnChart | 359, 0 | 462×280 | Category: Calendar[Fiscal Year] → Calendar[Fiscal Year Quarter] (drill hierarchy), Series: Calendar[Fiscal Year Quarter], Value: Count of Calendar[Date]. Sorted ascending. |
| EDP Logo | image | 1164, 0 | 116×49 | EDP_Logo_Final_Transparent. Links to SharePoint EDP site. |
| Table | tableEx | 0, 311 | 415×301 | Columns: Calendar[Date], Calendar[Fiscal Week], Calendar[Fiscal Year Quarter], Calendar[Fiscal Year Month] |
| Matrix | pivotTable | 527, 311 | 557×301 | Rows: Calendar[Fiscal Year], Columns: Calendar[Fiscal Year Quarter], Values: Count of Calendar[Date] |

### Visual Z-Order (layering)
- Image (z: 0) → behind
- Donut (z: 1000)
- Column Chart (z: 2000)
- Table (z: 3000)
- Matrix (z: 4000) → front

## Registered Resources (Images)

| Resource Name | Type | Usage |
|---------------|------|-------|
| EDP_Logo_Final_Black_350x150.png | Image | Dark background variant |
| EDP_Logo_Final_Transparent_350.png | Image | Primary logo (used on pages) |
| EDP_Logo_Final_White_350x150.png | Image | Light background variant |
| Hitachi-InspireTheNext.png | Image | Corporate branding top-right |
| Vector-Pattern_White_RGB_sm.png | Image | Page background pattern |
| powered_by_edp_text.png | Image | Footer branding |
| Hitachi.json | CustomTheme | Corporate theme file |

## Custom Visuals

- `massFilter` (community visual for advanced filtering)

## EDP Logo Link Configuration

The EDP logo on every page links to the SharePoint EDP site:
```json
{
  "visualLink": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "type": { "expr": { "Literal": { "Value": "'WebUrl'" } } },
      "webUrl": { "expr": { "Literal": { "Value": "'https://hitachivantara.sharepoint.com/sites/EnterpriseDataPlatform/SitePages/Enterprise-Data-Platform.aspx'" } } }
    }
  }]
}
```

## Implementation Steps (PBIR format)

When creating a new report from this template:

1. **Scaffold the PBIR project** with the folder structure:
   ```
   <ReportName>.Report/
     .platform
     definition.pbir
     definition/
       report.json
       version.json
       pages/
         pages.json
         <LandingPage>/
           page.json
           visuals/
         <EDPTemplate>/
           page.json
           visuals/
         <ImageAssets>/
           page.json
         <Version>/
           page.json
         <Instructions>/
           page.json
     StaticResources/
       RegisteredResources/
         (image files + theme JSON)
       SharedResources/
   ```

2. **Copy registered resources** (logos, background, theme) into `StaticResources/RegisteredResources/`

3. **Configure report.json** with theme collection and settings (see above)

4. **Create pages** with proper visibility settings (Image Assets, Version, Instructions = HiddenInViewMode)

5. **Place branded visuals** — EDP logo + Hitachi logo on Landing Page; EDP logo on each content page

6. **Set page background** on content pages using Vector-Pattern image at 35% transparency

7. **Bind data visuals** to the Calendar table (or your actual data model) following the position/size specs above

## Notes

- Always include the EDP logo with SharePoint link on every visible page (top-right area)
- Hidden pages (Image Assets, Version, Instructions) are for developer use only
- The Dataset Info table on the Landing Page shows last refresh time with a clickable timezone converter link
- Use the `Hitachi.json` custom theme for consistent corporate colors
- The template uses placeholder data from the Calendar table — replace with actual measures when building real reports
- Page background transparency at 35% ensures the pattern is subtle and doesn't distract from data
