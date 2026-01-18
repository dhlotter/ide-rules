---
name: google-tasks-manager
description: Interface with Google Tasks to create, manage, and sync tasks from your life operating system.
---

# Google Tasks Manager Skill

This skill allows you to interface with Google Tasks API to create and manage tasks, enabling seamless integration between your Obsidian-based life operating system and Google Tasks for actionable task management.

## Prerequisites

1. **Google Cloud Project**: A project with the Google Tasks API enabled
2. **Credentials**: A `credentials.json` file (can reuse from gmail-inbox-manager or google-calendar-manager)
3. **Authentication**: A valid `token.json` generated via the `auth.py` script

## Features

- ✅ Create tasks in Google Tasks from your life operating system
- ✅ List all task lists
- ✅ Query tasks with filters (by list, status, due date)
- ✅ Update existing tasks
- ✅ Complete/uncomplete tasks
- ✅ Add due dates and notes
- ✅ Sync tasks bidirectionally (optional)
- ✅ Export tasks to Obsidian markdown format

## Setup Instructions

### 1. Install Dependencies

Create a virtual environment and install required packages:

```bash
python3 -m venv ".agent/skills/google-tasks-manager/venv"
source ".agent/skills/google-tasks-manager/venv/bin/activate"
pip install -r ".agent/skills/google-tasks-manager/requirements.txt"
```

### 2. Setup Credentials

**Option A: Copy from existing skill**
```bash
cp ".agent/skills/gmail-inbox-manager/credentials.json" \
   ".agent/skills/google-tasks-manager/credentials.json"
```

**Option B: Create new credentials**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Tasks API
3. Create OAuth 2.0 credentials
4. Download as `credentials.json` and place in `.agent/skills/google-tasks-manager/`

### 3. Authenticate

Run the authentication script (opens browser for OAuth):

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/auth.py"
```

This will create `token.json` with your authenticated session.

### 4. Test the Connection

Verify the setup by listing your task lists:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"
```

## Usage

### List All Task Lists

Get all your Google Tasks lists:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"
```

Output includes list ID, title, and task count.

### Create a Task

Create a new task in Google Tasks:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/create_task.py" \
  --title "Task title" \
  --notes "Task description" \
  --list-id "LIST_ID" \
  --due-date "2026-01-20"
```

**Parameters:**
- `--title` (required): Task title
- `--notes` (optional): Task description/notes
- `--list-id` (optional): Target list ID (uses default list if not specified)
- `--due-date` (optional): Due date in YYYY-MM-DD format

### Query Tasks

List tasks with optional filters:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/query_tasks.py" \
  --list-id "LIST_ID" \
  --status "needsAction" \
  --limit 20
```

**Filters:**
- `--list-id`: Filter by specific task list
- `--status`: Filter by status (needsAction, completed, all)
- `--limit`: Maximum number of tasks to return (default: 50)

### Update a Task

Update an existing task:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/update_task.py" \
  --task-id "TASK_ID" \
  --list-id "LIST_ID" \
  --title "Updated title" \
  --due-date "2026-01-25"
```

### Complete a Task

Mark a task as complete:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/complete_task.py" \
  --task-id "TASK_ID" \
  --list-id "LIST_ID"
```

### Get Task Details

Retrieve detailed information about a specific task:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/get_task.py" \
  --task-id "TASK_ID" \
  --list-id "LIST_ID"
```

### Export to Markdown

Export tasks to Obsidian-friendly markdown format:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/export_to_markdown.py" \
  --list-id "LIST_ID" \
  --output-file "tasks.md" \
  --status "needsAction"
```

## Workflow Examples

### Planning in Obsidian → Send to Google Tasks

1. **Identify tasks** from your Obsidian notes/planning
2. **Extract key details**: title, description, due date
3. **Create task** using `create_task.py`
4. **Store task ID** in your Obsidian note for reference (optional)

Example agent workflow:
```
User: "Create a Google Tasks task to review the Q1 budget by Friday"

Agent:
1. Runs list_task_lists.py to find the right list
2. Runs create_task.py with:
   - title: "Review Q1 budget"
   - due-date: "2026-01-24" (next Friday)
   - list-id: [Work list ID]
3. Returns task ID and confirmation
```

### Sync Tasks Back to Obsidian

1. **Query tasks** from Google Tasks using `query_tasks.py`
2. **Parse results** and identify new/updated tasks
3. **Update Obsidian notes** with task status or create new task notes

### Daily Planning Integration

1. **Morning**: Query today's tasks from Google Tasks
2. **Review**: Display in Obsidian daily note
3. **Evening**: Create new tasks from daily note reflections
4. **Sync**: Mark completed tasks in Google Tasks

## API Notes

- All scripts output JSON for easy parsing
- Use `--help` flag on any script to see all available options
- Task IDs and List IDs are returned in API responses
- Google Tasks API has generous rate limits
- Tokens expire and will be automatically refreshed

## Security

- API credentials are stored in `.agent/skills/google-tasks-manager/credentials.json`
- OAuth tokens stored in `.agent/skills/google-tasks-manager/token.json`
- Both files are gitignored by default
- Never commit credentials to version control

## Troubleshooting

### Authentication Errors
- Re-run `auth.py` to refresh your token
- Verify Google Tasks API is enabled in your project
- Check if OAuth consent screen is configured

### Task Creation Fails
- Verify the list ID exists using `list_task_lists.py`
- Check date format is YYYY-MM-DD
- Ensure you have write permissions

### No Tasks Returned
- Check if you have tasks in the specified list
- Verify filter parameters are correct
- Try without filters to see all tasks

## Advanced Usage

### Batch Task Creation

Create multiple tasks from a JSON file:

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/batch_create.py" \
  --input-file "tasks.json"
```

## Resources

- [Google Tasks API Documentation](https://developers.google.com/tasks)
- [Google Cloud Console](https://console.cloud.google.com/)
- Skill source: `.agent/skills/google-tasks-manager/`
