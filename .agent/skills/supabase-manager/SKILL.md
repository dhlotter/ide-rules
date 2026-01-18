---
name: supabase-manager
description: Comprehensive Supabase project management - database queries, migrations, authentication, logs, edge functions, and more.
---

# Supabase Manager Skill

This skill provides comprehensive management capabilities for Supabase projects, enabling you to interact with databases, manage migrations, monitor authentication, review logs, and manage edge functions across different projects.

## Prerequisites

1. **Supabase CLI**: Install the Supabase CLI globally
2. **Supabase Account**: Access to one or more Supabase projects
3. **Project Configuration**: Project reference ID and access tokens
4. **Python 3.8+**: For advanced scripting capabilities

## Features

- ✅ **Project Discovery**: Automatically detect all projects from your Supabase account
- ✅ **Auto-Detection**: Automatically switch project based on the repository you are currently in
- ✅ **Database Queries**: Execute SQL queries and view results
- ✅ **Migration Management**: Create, apply, and rollback migrations
- ✅ **Authentication**: View users, sessions, and auth logs
- ✅ **Edge Functions**: Deploy, invoke, and monitor edge functions
- ✅ **Logs**: View database, auth, and function logs
- ✅ **Storage**: Manage buckets and files
- ✅ **Real-time**: Monitor real-time subscriptions
- ✅ **Multi-Project**: Seamlessly work with multiple projects

## Setup Instructions

### 1. Install Supabase CLI

```bash
brew install supabase/tap/supabase
```

Verify installation:
```bash
supabase --version
```

### 2. Install Python Dependencies

The skill includes a setup script that creates the venv and installs dependencies:

```bash
# This happened automatically during setup
```

### 3. Login to Supabase

Authenticate with your Supabase account:

```bash
supabase login
```

### 4. Discover Projects

Automatically import all projects from your account:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/discover_projects.py"
```

## Core Capabilities

### Project Management

#### Discover All Your Projects

Fetch every project associated with your Supabase account:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/discover_projects.py"
```

#### Auto-Detect Project from Current Directory

If you are in a repository linked with Supabase (contains `.supabase/project-ref`), use this to set the active project:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/detect_current_project.py"
```

#### Switch Active Project

Change the active project context:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/switch_project.py" \
  --name "my-project"
```

#### Get Project Status

View comprehensive project status:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/project_status.py" \
  --project "my-project"
```

### Database Operations

#### Execute SQL Query

Run SQL queries against your database:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/query_db.py" \
  --project "my-project" \
  --query "SELECT * FROM users LIMIT 10"
```

With query from file:
```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/query_db.py" \
  --project "my-project" \
  --file "query.sql"
```

#### Inspect Database Schema

View tables, columns, and relationships:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/inspect_schema.py" \
  --project "my-project" \
  --table "users"
```

#### Export Data

Export table data to JSON or CSV:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/export_data.py" \
  --project "my-project" \
  --table "users" \
  --format "json" \
  --output "users.json"
```

### Migration Management

#### Create Migration

Generate a new migration file:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/create_migration.py" \
  --project "my-project" \
  --name "add_user_profiles"
```

#### List Migrations

View all migrations and their status:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_migrations.py" \
  --project "my-project"
```

#### Apply Migrations

Push migrations to your database:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/apply_migrations.py" \
  --project "my-project"
```

#### Rollback Migration

Revert the last migration:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/rollback_migration.py" \
  --project "my-project" \
  --steps 1
```

### Authentication Management

#### List Users

View all authenticated users:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_users.py" \
  --project "my-project" \
  --limit 50
```

#### Get User Details

View detailed user information:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/get_user.py" \
  --project "my-project" \
  --user-id "uuid-here"
```

#### View Auth Logs

Monitor authentication events:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/auth_logs.py" \
  --project "my-project" \
  --hours 24
```

### Edge Functions

#### List Functions

View all edge functions:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_functions.py" \
  --project "my-project"
```

#### Deploy Function

Deploy an edge function:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/deploy_function.py" \
  --project "my-project" \
  --function "my-function"
```

#### Invoke Function

Test an edge function:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/invoke_function.py" \
  --project "my-project" \
  --function "my-function" \
  --payload '{"key": "value"}'
```

#### View Function Logs

Monitor edge function logs:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/function_logs.py" \
  --project "my-project" \
  --function "my-function" \
  --tail
```

### Logs & Monitoring

#### View Database Logs

Monitor database activity:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/db_logs.py" \
  --project "my-project" \
  --level "error" \
  --tail
```

#### View All Logs

Aggregate view of all logs:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/view_logs.py" \
  --project "my-project" \
  --type "all" \
  --hours 1
```

### Storage Management

#### List Buckets

View all storage buckets:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_buckets.py" \
  --project "my-project"
```

#### List Files

View files in a bucket:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_files.py" \
  --project "my-project" \
  --bucket "avatars" \
  --path "public/"
```

## Workflow Examples

### Daily Project Health Check

```bash
# 1. Check project status
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/project_status.py" \
  --project "my-project"

# 2. Review recent errors
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/view_logs.py" \
  --project "my-project" \
  --level "error" \
  --hours 24

# 3. Check auth activity
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/auth_logs.py" \
  --project "my-project" \
  --hours 24
```

### Deploy New Feature

```bash
# 1. Create migration
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/create_migration.py" \
  --project "my-project" \
  --name "add_new_feature"

# 2. Apply migration
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/apply_migrations.py" \
  --project "my-project"

# 3. Deploy edge function
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/deploy_function.py" \
  --project "my-project" \
  --function "new-feature-handler"

# 4. Test function
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/invoke_function.py" \
  --project "my-project" \
  --function "new-feature-handler" \
  --payload '{"test": true}'
```

### Debug Production Issue

```bash
# 1. View recent errors
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/view_logs.py" \
  --project "my-project" \
  --level "error" \
  --hours 2

# 2. Check database for anomalies
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/query_db.py" \
  --project "my-project" \
  --query "SELECT * FROM error_logs ORDER BY created_at DESC LIMIT 20"

# 3. Review auth issues
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/auth_logs.py" \
  --project "my-project" \
  --hours 2 \
  --filter "failed"
```

## Configuration

### Projects Config File

The skill maintains a `projects.json` file with your project configurations:

```json
{
  "projects": [
    {
      "name": "my-project",
      "ref": "abcdefghijklmnop",
      "path": "/path/to/project",
      "url": "https://abcdefghijklmnop.supabase.co",
      "active": true
    }
  ],
  "active_project": "my-project"
}
```

### Environment Variables

You can also use environment variables:

```bash
export SUPABASE_PROJECT_REF="your-project-ref"
export SUPABASE_ACCESS_TOKEN="your-access-token"
export SUPABASE_DB_PASSWORD="your-db-password"
```

## Security

- **Access Tokens**: Stored securely via Supabase CLI
- **Database Passwords**: Never committed to version control
- **Projects Config**: Added to `.gitignore` by default
- **Service Role Keys**: Use with caution, never expose in client code

## Troubleshooting

### CLI Not Found
```bash
# Install Supabase CLI
brew install supabase/tap/supabase
```

### Authentication Failed
```bash
# Re-login to Supabase
supabase login
```

### Project Not Linked
```bash
# Link your project
cd /path/to/project
supabase link --project-ref YOUR_PROJECT_REF
```

### Migration Errors
```bash
# Check migration status
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/list_migrations.py" \
  --project "my-project"

# Rollback if needed
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/rollback_migration.py" \
  --project "my-project"
```

## Advanced Usage

### Custom SQL Scripts

Create reusable SQL scripts in `scripts/sql/`:

```sql
-- scripts/sql/user_stats.sql
SELECT 
  COUNT(*) as total_users,
  COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as new_users_7d,
  COUNT(CASE WHEN last_sign_in_at > NOW() - INTERVAL '7 days' THEN 1 END) as active_users_7d
FROM auth.users;
```

Execute:
```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/query_db.py" \
  --project "my-project" \
  --file ".agent/skills/supabase-manager/scripts/sql/user_stats.sql"
```

### Automated Backups

Schedule regular database backups:

```bash
".agent/skills/supabase-manager/venv/bin/python" \
  ".agent/skills/supabase-manager/scripts/backup_db.py" \
  --project "my-project" \
  --output "/backups/$(date +%Y%m%d).sql"
```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase CLI Reference](https://supabase.com/docs/reference/cli)
- [Supabase Management API](https://supabase.com/docs/reference/api)
- Skill source: `.agent/skills/supabase-manager/`

## What I Need From You

To complete this skill setup, please provide:

1. **Project Information**:
   - Project name(s) you want to manage
   - Project reference ID(s) (from Supabase dashboard URL)
   - Project path(s) on your local machine (if applicable)

2. **Access Credentials**:
   - Have you already run `supabase login`?
   - Do you have your database password(s)?

3. **Use Cases**:
   - What are your primary use cases? (migrations, queries, logs, functions, etc.)
   - Are there specific operations you perform frequently?
   - Do you work with multiple Supabase projects?

4. **Preferences**:
   - Output format preferences (JSON, table, markdown)?
   - Any specific naming conventions for migrations?
   - Preferred log levels and monitoring intervals?
