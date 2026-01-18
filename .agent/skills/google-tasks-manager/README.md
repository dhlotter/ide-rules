# Google Tasks Manager Skill

A comprehensive skill for interfacing with Google Tasks API to manage tasks from your Obsidian-based life operating system.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd "/Users/dhlotter/My Drive/obsidian/easyentropy"
   python3 -m venv ".agent/skills/google-tasks-manager/venv"
   source ".agent/skills/google-tasks-manager/venv/bin/activate"
   pip install -r ".agent/skills/google-tasks-manager/requirements.txt"
   ```

2. **Copy credentials from existing skill:**
   ```bash
   cp ".agent/skills/gmail-inbox-manager/credentials.json" \
      ".agent/skills/google-tasks-manager/credentials.json"
   ```

3. **Authenticate:**
   ```bash
   ".agent/skills/google-tasks-manager/venv/bin/python" \
     ".agent/skills/google-tasks-manager/scripts/auth.py"
   ```

4. **Test the connection:**
   ```bash
   ".agent/skills/google-tasks-manager/venv/bin/python" \
     ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"
   ```

## Available Scripts

### Core Operations

- **`auth.py`** - OAuth authentication and token management
- **`list_task_lists.py`** - List all Google Tasks lists
- **`create_task.py`** - Create a new task
- **`query_tasks.py`** - Query tasks with filters
- **`get_task.py`** - Get details of a specific task
- **`update_task.py`** - Update an existing task
- **`complete_task.py`** - Mark a task as complete

### Advanced Operations

- **`batch_create.py`** - Create multiple tasks from JSON
- **`export_to_markdown.py`** - Export tasks to Obsidian markdown

## Example Workflows

### Create a Task from Planning

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/create_task.py" \
  --title "Review Q1 Budget" \
  --notes "Focus on marketing and R&D expenses" \
  --due-date "2026-01-24"
```

### Export Today's Tasks to Markdown

```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/export_to_markdown.py" \
  --status needsAction \
  --output-file "10-Daily/2026-01-18-tasks.md"
```

### Batch Create Tasks

Create a `tasks.json` file:
```json
{
  "tasks": [
    {
      "title": "Morning workout",
      "notes": "30 minutes cardio",
      "due_date": "2026-01-19"
    },
    {
      "title": "Review pull requests",
      "notes": "Focus on the new feature branch",
      "due_date": "2026-01-18"
    }
  ]
}
```

Then run:
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/batch_create.py" \
  --input-file "tasks.json"
```

## Integration with Life Operating System

### Daily Planning Workflow

1. **Morning Review:**
   - Query today's tasks from Google Tasks
   - Display in daily note for context

2. **Throughout the Day:**
   - Create quick tasks as they come up
   - Update due dates as needed

3. **Evening Reflection:**
   - Export completed tasks to daily note
   - Plan tomorrow's tasks

### Project Planning Integration

When planning projects in Obsidian:

1. Break down project into actionable tasks
2. Use `batch_create.py` to send tasks to Google Tasks
3. Store task IDs in project notes for reference
4. Sync status back to Obsidian periodically

## API Reference

### Task Object Structure

```json
{
  "id": "task_id",
  "title": "Task title",
  "notes": "Task description",
  "status": "needsAction",
  "due": "2026-01-24T00:00:00.000Z",
  "completed": null,
  "parent": null,
  "position": "00000000000000000000",
  "updated": "2026-01-18T08:00:00.000Z"
}
```

### Status Values

- `needsAction` - Task is not completed
- `completed` - Task is completed

## Advantages Over TickTick

✅ **No separate authentication** - Uses existing Google credentials  
✅ **Native Google integration** - Works with Gmail, Calendar, etc.  
✅ **Free** - No subscription required  
✅ **Simple API** - Straightforward task management  
✅ **Cross-platform** - Available on all devices with Google Tasks app  
✅ **Reliable** - Backed by Google infrastructure  

## Troubleshooting

### Common Issues

**Authentication fails:**
- Verify credentials.json is present
- Check if Google Tasks API is enabled in your project
- Try re-running `auth.py`

**Tasks not appearing:**
- Verify the list ID exists
- Check if tasks are filtered out by status
- Try querying without filters

**Date parsing errors:**
- Use YYYY-MM-DD format for dates
- Ensure dates are valid

## Security Notes

- Credentials are stored in `.agent/skills/google-tasks-manager/credentials.json`
- OAuth tokens stored in `.agent/skills/google-tasks-manager/token.json`
- Both files should never be committed to version control
- Tokens are automatically refreshed when expired

## Resources

- [Google Tasks API Documentation](https://developers.google.com/tasks)
- [Google Cloud Console](https://console.cloud.google.com/)
- Skill location: `.agent/skills/google-tasks-manager/`

---

*Created for the EasyEntropy Life Operating System*
