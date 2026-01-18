# Supabase Manager - Quick Reference

## Setup (One-time)

```bash
# 1. Install CLI
brew install supabase/tap/supabase

# 2. Login
supabase login

# 3. Setup Python
python3 -m venv ".agent/skills/supabase-manager/venv"
source ".agent/skills/supabase-manager/venv/bin/activate"
pip install -r ".agent/skills/supabase-manager/requirements.txt"

# 4. Add project
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/configure_projects.py" \
  --add --name "PROJECT_NAME" --ref "PROJECT_REF" --path "/path/to/project"
```

## Quick Commands

All commands assume you're using the venv Python:
```bash
PYTHON=".agent/skills/supabase-manager/venv/bin/python"
SCRIPTS=".agent/skills/supabase-manager/scripts"
```

### Projects
```bash
# List all projects
$PYTHON $SCRIPTS/list_projects.py

# Switch project
$PYTHON $SCRIPTS/switch_project.py --name "PROJECT_NAME"

# Get status
$PYTHON $SCRIPTS/project_status.py
```

### Database
```bash
# Query
$PYTHON $SCRIPTS/query_db.py --query "SELECT * FROM users LIMIT 10"

# Query from file
$PYTHON $SCRIPTS/query_db.py --file "query.sql"

# Inspect schema
$PYTHON $SCRIPTS/inspect_schema.py

# Inspect table
$PYTHON $SCRIPTS/inspect_schema.py --table "users"
```

### Migrations
```bash
# List
$PYTHON $SCRIPTS/list_migrations.py

# Create
$PYTHON $SCRIPTS/create_migration.py --name "migration_name"

# Apply
$PYTHON $SCRIPTS/apply_migrations.py
```

### Logs
```bash
# All logs (last hour)
$PYTHON $SCRIPTS/view_logs.py

# Database logs
$PYTHON $SCRIPTS/view_logs.py --type "db" --hours 2

# Auth logs
$PYTHON $SCRIPTS/auth_logs.py --hours 24

# Tail logs (real-time)
$PYTHON $SCRIPTS/view_logs.py --tail
```

## Output Formats

Add `--format table` for tabular output:
```bash
$PYTHON $SCRIPTS/list_projects.py --format table
```

## Common Workflows

### Daily Health Check
```bash
$PYTHON $SCRIPTS/project_status.py
$PYTHON $SCRIPTS/view_logs.py --type "all" --level "error" --hours 24
$PYTHON $SCRIPTS/auth_logs.py --hours 24
```

### Deploy Migration
```bash
$PYTHON $SCRIPTS/create_migration.py --name "add_feature"
# Edit the migration file
$PYTHON $SCRIPTS/apply_migrations.py
```

### Debug Issue
```bash
$PYTHON $SCRIPTS/view_logs.py --type "db" --level "error" --hours 2
$PYTHON $SCRIPTS/query_db.py --query "SELECT * FROM error_logs ORDER BY created_at DESC LIMIT 20"
```

## Project-Specific Commands

Use `--project "PROJECT_NAME"` with any command:
```bash
$PYTHON $SCRIPTS/query_db.py --project "production" --query "SELECT COUNT(*) FROM users"
```

## Tips

1. **Set up aliases** in your shell:
   ```bash
   alias sb-query='".agent/skills/supabase-manager/venv/bin/python" ".agent/skills/supabase-manager/scripts/query_db.py"'
   alias sb-logs='".agent/skills/supabase-manager/venv/bin/python" ".agent/skills/supabase-manager/scripts/view_logs.py"'
   ```

2. **Save common queries** in `.agent/skills/supabase-manager/scripts/sql/`

3. **Use table format** for better readability in terminal:
   ```bash
   $PYTHON $SCRIPTS/list_projects.py --format table
   ```

4. **Chain commands** for workflows:
   ```bash
   $PYTHON $SCRIPTS/create_migration.py --name "new_feature" && \
   $PYTHON $SCRIPTS/apply_migrations.py
   ```
