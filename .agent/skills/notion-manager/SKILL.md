---
name: notion-manager
description: Fetches and manages Notion databases and pages/notes.
---

# Notion Manager Skill

This skill allows the agent to interact with your Notion workspace, including reading databases, pages, and notes, as well as creating and updating content.

## Prerequisites

1. **Notion Integration**: Create a Notion integration at https://www.notion.so/my-integrations
2. **Integration Token**: Copy your integration token (starts with `secret_`)
3. **Page/Database Access**: Share the pages/databases you want to access with your integration

## Usage

### 1. Setup (One-time)
Store your Notion integration token:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/setup.py"
```

This will prompt you for your integration token and save it to `.agent/skills/notion-manager/token.txt`.

### 2. List Databases
List all databases that your integration has access to:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/list_databases.py"
```

### 3. Query Database
Query entries from a specific database:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/query_database.py" --database-id "DATABASE_ID" --limit 10
```

### 4. Read Page
Read the content of a specific Notion page:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/read_page.py" --page-id "PAGE_ID"
```

### 5. Search Content
Search across your Notion workspace:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/search.py" --query "your search query" --limit 10
```

### 6. Create Page
Create a new page in a database or as a child of another page:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/create_page.py" --parent-id "PARENT_ID" --title "Page Title" --content "Page content"
```

### 7. Update Page
Update an existing Notion page:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/update_page.py" --page-id "PAGE_ID" --title "New Title" --content "New content"
```

### 8. Create Database Entry
Add a new entry to a database:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/create_database_entry.py" --database-id "DATABASE_ID" --properties '{"Name": "Entry name", "Status": "In Progress"}'
```

### 9. Update Database Entry
Update an existing database entry:
```bash
".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/update_database_entry.py" --page-id "PAGE_ID" --properties '{"Status": "Completed"}'
```

## Workflow

### Reading and Summarizing
1. **Search/List**: The agent uses `list_databases.py` or `search.py` to find relevant content
2. **Fetch**: Use `query_database.py` or `read_page.py` to get the detailed content
3. **Analyze**: The agent processes the content
4. **Summarize**: Provide insights, summaries, or save to Obsidian vault

### Creating and Updating
1. **Identify Target**: Find the database or parent page ID
2. **Prepare Content**: Structure the content according to Notion's format
3. **Execute**: Use `create_page.py`, `update_page.py`, or database scripts
4. **Verify**: Optionally read back the content to confirm changes

## Setup Instructions

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv ".agent/skills/notion-manager/venv"
   source ".agent/skills/notion-manager/venv/bin/activate"
   pip install -r ".agent/skills/notion-manager/requirements.txt"
   ```

2. Run the setup script to store your Notion integration token:
   ```bash
   ".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/setup.py"
   ```

3. Test the connection by listing databases:
   ```bash
   ".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/list_databases.py"
   ```

## Notes

- All scripts output JSON for easy parsing by the agent
- Use `--help` flag on any script to see all available options
- Page IDs and Database IDs can be found in the Notion URL (e.g., `notion.so/Page-Title-{page-id}`)
- The integration can only access pages/databases that have been explicitly shared with it
