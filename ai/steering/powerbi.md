---
inclusion: manual
---
<!------------------------------------------------------------------------------------
inclusion: always
   Add rules to this file or a short description that will apply across all your workspaces.
   
   Learn about inclusion modes: https://kiro.dev/docs/steering/#inclusion-modes
-------------------------------------------------------------------------------------> 
When working with powerbi files, prioritize using the PowerBi-Modeling-MCP server over Power BI CLI tools. Use the MCP server, as it doesnt need restarting PowerBi desktop. Prefer the MCP server especially when working with the Semantic Model. Leverag Power Bi CLI only for the report layer.

Look for a Calendar table. If one is not available, ask if one should be created and if it should be a HV Fiscal Calendar or a normal calendar. If a normal calendar use the skill power-bi-calendar-table.

Look for dataset info table. If one is not available, ask if one should be created and if one should be created, use power-bi-dataset-info skill.


<!-- pbi-cli:start -->
# Power BI CLI (pbi-cli)

When working with Power BI, DAX, semantic models, or data modeling,
invoke the relevant pbi-cli skill before responding:

**Semantic Model (requires `pbi connect`):**
- **power-bi-dax** -- DAX queries, measures, calculations
- **power-bi-modeling** -- tables, columns, measures, relationships
- **power-bi-deployment** -- TMDL export/import, transactions, diff
- **power-bi-docs** -- model documentation, data dictionary
- **power-bi-partitions** -- partitions, M expressions, data sources
- **power-bi-security** -- RLS roles, perspectives, access control
- **power-bi-diagnostics** -- troubleshooting, tracing, setup

**Report Layer (no connection needed):**
- **power-bi-report** -- scaffold, validate, preview PBIR reports
- **power-bi-visuals** -- add, bind, update, bulk-manage visuals
- **power-bi-pages** -- pages, bookmarks, visibility, drillthrough
- **power-bi-themes** -- themes, conditional formatting, styling
- **power-bi-filters** -- page and visual filters (TopN, date, categorical)
- **power-bi-custom-visuals** -- vibe-code .pbiviz custom visuals (TS scaffold, tsc loop, package, import)

Critical: Multi-line DAX (VAR/RETURN) cannot be passed via `-e`.
Use `--file` or stdin piping instead. See power-bi-dax skill.
<!-- pbi-cli:end -->
