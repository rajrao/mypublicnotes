---
name: Power BI Documentation
description: Auto-document Power BI semantic models by extracting metadata, generating documentation, and cataloging all model objects using pbi-cli. Invoke this skill whenever the user says "document this model", "what's in this model", "list everything", "data dictionary", "model inventory", "audit contents", "catalog", "describe the model", or wants to understand what objects exist in a semantic model.
tools: pbi-cli
---

# Power BI Documentation Skill

Generate comprehensive documentation for Power BI semantic models.

## Prerequisites

```bash
pipx install pbi-cli-tool
pbi-cli skills install
pbi connect
```

## Quick Model Overview

```bash
pbi --json model get       # Model metadata
pbi --json model stats     # Table/measure/column counts
```

## Catalog All Objects

```bash
# Tables and their structure
pbi --json table list
pbi --json table get Sales
pbi --json table schema Sales

# All measures
pbi --json measure list

# Individual measure details
pbi --json measure get "Total Revenue" --table Sales

# Columns per table
pbi --json column list --table Sales
pbi --json column list --table Products

# Relationships
pbi --json relationship list

# Security roles
pbi --json security-role list

# Hierarchies
pbi --json hierarchy list --table Date

# Calculation groups
pbi --json calc-group list

# Perspectives
pbi --json perspective list

# Named expressions (M queries)
pbi --json expression list

# Partitions
pbi --json partition list --table Sales

# Calendar/date tables
pbi --json calendar list
```

## Export Full Model as TMDL

```bash
pbi database export-tmdl ./model-docs/
```

This creates a human-readable text representation of the entire model.

## Workflow: Generate Model Documentation

Run these commands to gather all information needed for documentation:

```bash
# Step 1: Model overview
pbi --json model get > model-meta.json
pbi --json model stats > model-stats.json

# Step 2: All tables
pbi --json table list > tables.json

# Step 3: All measures
pbi --json measure list > measures.json

# Step 4: All relationships
pbi --json relationship list > relationships.json

# Step 5: Security roles
pbi --json security-role list > security-roles.json

# Step 6: Column details per table (loop through tables)
pbi --json column list --table Sales > columns-sales.json
pbi --json column list --table Products > columns-products.json

# Step 7: Full TMDL export
pbi database export-tmdl ./tmdl-export/
```

Then assemble these JSON files into markdown or HTML documentation.

## Workflow: Data Dictionary

For each table, extract columns and their types:

```bash
# Get schema for key tables
pbi --json table schema Sales
pbi --json table schema Products
pbi --json table schema Calendar
```

## Workflow: Measure Catalog

Create a complete measure inventory:

```bash
# List all measures with expressions
pbi --json measure list

# Export full model as TMDL (includes all measure definitions)
pbi database export-tmdl ./tmdl-export/
```

## Culture Management

For multi-language models:

```bash
# List cultures (locales)
pbi --json advanced culture list

# Create a culture for localization
pbi advanced culture create "fr-FR"

# Delete a culture
pbi advanced culture delete "fr-FR"
```

## Best Practices

- Always use `--json` flag for machine-readable output
- Export TMDL alongside JSON for complete documentation
- Run documentation generation as part of CI/CD pipeline
- Keep documentation in version control alongside TMDL exports
- Include relationship diagrams (generate from `pbi --json relationship list`)
- Document measure business logic, not just DAX expressions
- Tag measures by business domain using display folders
