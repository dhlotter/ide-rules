# Google Tasks Manager - Quick Reference

## Setup (One-time)

```bash
# 1. Create virtual environment and install dependencies
python3 -m venv ".agent/skills/google-tasks-manager/venv"
source ".agent/skills/google-tasks-manager/venv/bin/activate"
pip install -r ".agent/skills/google-tasks-manager/requirements.txt"

# 2. Credentials already copied! ✓

# 3. Authenticate (opens browser)
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/auth.py"

# 4. Test connection
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"
```

## Common Commands

### List Task Lists
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"
```

### Create Task
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/create_task.py" \
  --title "Task title" \
  --notes "Description" \
  --due-date "2026-01-20"
```

### Query Tasks
```bash
# All active tasks
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/query_tasks.py"

# Tasks in specific list
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/query_tasks.py" \
  --list-id "LIST_ID"

# All tasks (including completed)
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/query_tasks.py" \
  --status all
```

### Complete Task
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/complete_task.py" \
  --task-id "TASK_ID" \
  --list-id "LIST_ID"
```

### Update Task
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/update_task.py" \
  --task-id "TASK_ID" \
  --list-id "LIST_ID" \
  --title "New title" \
  --due-date "2026-01-25"
```

### Export to Markdown
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/export_to_markdown.py" \
  --output-file "tasks.md" \
  --status needsAction
```

### Batch Create
```bash
".agent/skills/google-tasks-manager/venv/bin/python" \
  ".agent/skills/google-tasks-manager/scripts/batch_create.py" \
  --input-file "tasks.json"
```

## Status Values

- `needsAction` - Task is not completed
- `completed` - Task is completed
- `all` - Both completed and active tasks

## Date Format

Use `YYYY-MM-DD` format for dates:
- `2026-01-18`
- `2026-12-31`

## Tips

1. **Get List IDs**: Run `list_task_lists.py` first to find list IDs
2. **Default List**: Use `@default` or omit `--list-id` for default list
3. **JSON Output**: All scripts output JSON for easy parsing
4. **Help**: Add `--help` to any script to see all options
5. **Batch Operations**: Use `batch_create.py` for multiple tasks

## Agent Usage Examples

When the agent needs to create a task:
1. Parse user request for task details
2. Run `list_task_lists.py` to find appropriate list (optional)
3. Run `create_task.py` with extracted details
4. Return task ID and confirmation

When the agent needs to plan the day:
1. Run `query_tasks.py` to get today's tasks
2. Run `export_to_markdown.py` to create daily task list
3. Present formatted tasks to user

## Advantages

✅ Uses existing Google credentials  
✅ No separate authentication needed  
✅ Free - no subscription  
✅ Native Google integration  
✅ Simple and reliable
