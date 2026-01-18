# Supabase Manager Skill

A comprehensive skill for managing Supabase projects, databases, migrations, authentication, and more.

## Quick Start

1. **Install Supabase CLI**:
   ```bash
   brew install supabase/tap/supabase
   ```

2. **Login to Supabase**:
   ```bash
   supabase login
   ```

3. **Setup Python environment**:
   ```bash
   python3 -m venv ".agent/skills/supabase-manager/venv"
   source ".agent/skills/supabase-manager/venv/bin/activate"
   pip install -r ".agent/skills/supabase-manager/requirements.txt"
   ```

4. **Configure your first project**:
   ```bash
   ".agent/skills/supabase-manager/venv/bin/python" \
     ".agent/skills/supabase-manager/scripts/configure_projects.py" \
     --add \
     --name "my-project" \
     --ref "your-project-ref" \
     --path "/path/to/project"
   ```

## Features

- ✅ Multi-project management
- ✅ Database queries and schema inspection
- ✅ Migration creation and management
- ✅ Authentication monitoring
- ✅ Comprehensive logging
- ✅ Edge function management (via CLI)
- ✅ Storage management (via CLI)

## Common Commands

### Project Management
```bash
# List projects
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_projects.py"

# Switch project
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/switch_project.py" \
  --name "my-project"

# Get status
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/project_status.py"
```

### Database Operations
```bash
# Run query
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/query_db.py" \
  --query "SELECT * FROM users LIMIT 10"

# Inspect schema
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/inspect_schema.py" \
  --table "users"
```

### Migrations
```bash
# Create migration
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/create_migration.py" \
  --name "add_user_profiles"

# List migrations
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_migrations.py"

# Apply migrations
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/apply_migrations.py"
```

### Monitoring
```bash
# View logs
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/view_logs.py" \
  --type "db" \
  --hours 1

# Auth logs
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/auth_logs.py" \
  --hours 24
```

## Documentation

See `SKILL.md` for complete documentation.

## Directory Structure

```
supabase-manager/
├── SKILL.md              # Complete skill documentation
├── README.md             # This file
├── QUICKREF.md           # Quick reference guide
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── projects.json        # Project configurations (auto-generated)
├── scripts/             # Python scripts
│   ├── supabase_api.py  # Core API module
│   ├── configure_projects.py
│   ├── list_projects.py
│   ├── switch_project.py
│   ├── project_status.py
│   ├── query_db.py
│   ├── inspect_schema.py
│   ├── list_migrations.py
│   ├── create_migration.py
│   ├── apply_migrations.py
│   ├── view_logs.py
│   └── auth_logs.py
└── examples/            # Example configurations and queries
```

## Support

For issues or questions, refer to:
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase CLI Reference](https://supabase.com/docs/reference/cli)
