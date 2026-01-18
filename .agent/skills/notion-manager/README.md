# Notion Manager Skill

A comprehensive skill for interacting with Notion workspaces, allowing you to read, create, and update databases, pages, and notes.

## Quick Start

1. **Install dependencies:**
   ```bash
   bash ".agent/skills/notion-manager/scripts/setup.sh"
   ```

2. **Set up your Notion integration:**
   - Go to https://www.notion.so/my-integrations
   - Click "+ New integration"
   - Name it (e.g., "Obsidian Agent")
   - Copy the "Internal Integration Token"

3. **Save your token:**
   ```bash
   ".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/setup.py"
   ```

4. **Share pages with your integration:**
   - Open any Notion page or database you want to access
   - Click "Share" in the top right
   - Invite your integration by name

5. **Test the connection:**
   ```bash
   ".agent/skills/notion-manager/venv/bin/python" ".agent/skills/notion-manager/scripts/list_databases.py"
   ```

## Available Scripts

### Read Operations

- **list_databases.py** - List all accessible databases
- **query_database.py** - Query entries from a specific database
- **read_page.py** - Read the content of a specific page
- **search.py** - Search across your Notion workspace

### Write Operations

- **create_page.py** - Create a new page
- **update_page.py** - Update an existing page
- **create_database_entry.py** - Add a new entry to a database
- **update_database_entry.py** - Update an existing database entry

## Usage Examples

### List all databases
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/list_databases.py"
```

### Query a database
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/query_database.py" \
  --database-id "YOUR_DATABASE_ID" \
  --limit 10
```

### Read a page with its content
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/read_page.py" \
  --page-id "YOUR_PAGE_ID" \
  --include-children
```

### Search for content
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/search.py" \
  --query "project ideas" \
  --limit 5
```

### Create a new page
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/create_page.py" \
  --parent-id "YOUR_PARENT_PAGE_ID" \
  --title "My New Page" \
  --content "This is the page content"
```

### Update a page
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/update_page.py" \
  --page-id "YOUR_PAGE_ID" \
  --title "Updated Title" \
  --append-content "Additional content"
```

### Create a database entry
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/create_database_entry.py" \
  --database-id "YOUR_DATABASE_ID" \
  --properties '{"Name": "New Task", "Status": "To Do"}'
```

### Update a database entry
```bash
".agent/skills/notion-manager/venv/bin/python" \
  ".agent/skills/notion-manager/scripts/update_database_entry.py" \
  --page-id "YOUR_ENTRY_PAGE_ID" \
  --properties '{"Status": "Completed"}'
```

## Tips

- **Finding IDs**: Page and database IDs can be found in the Notion URL. For example:
  - `https://notion.so/My-Page-abc123def456` → ID is `abc123def456`
  - You can also use the search script to find pages and get their IDs

- **Property Types**: When creating or updating database entries, the scripts will try to infer the property type. For best results:
  - Use "Name" or "Title" for the main title property
  - For other properties, the script defaults to rich_text
  - Check your database schema in Notion if you need specific property types

- **Permissions**: Your integration can only access pages and databases that have been explicitly shared with it

## Troubleshooting

- **"Token file not found"**: Run `setup.py` first to save your integration token
- **"Could not find object"**: Make sure the page/database is shared with your integration
- **"Invalid request URL"**: Check that your page ID or database ID is correct

## Files Overview

```
.agent/skills/notion-manager/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── token.txt                   # Your Notion integration token (created by setup.py)
├── venv/                       # Python virtual environment
└── scripts/
    ├── setup.sh                # Initial setup script
    ├── setup.py                # Token setup script
    ├── utils.py                # Shared utilities
    ├── list_databases.py       # List databases
    ├── query_database.py       # Query database entries
    ├── read_page.py            # Read page content
    ├── search.py               # Search workspace
    ├── create_page.py          # Create new page
    ├── update_page.py          # Update page
    ├── create_database_entry.py # Create database entry
    └── update_database_entry.py # Update database entry
```
