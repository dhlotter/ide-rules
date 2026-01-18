---
description: Create a new project in the 20-Projects directory with standardized boilerplate
---

1. Ask the user for the name of the new project and a brief description.
2. Get the current date in `YYYY-MM-DD` format.
// turbo
3. Create a sanitized project slug by converting the name to lowercase and replacing spaces with hyphens.
4. Construct the project folder name: `${current_date}-${project_slug}`.
5. Define the full project path: `/Users/dhlotter/My Drive/obsidian/easyentropy/20-Projects/${folder_name}`.
// turbo
6. Create the project directory.
7. Create a `.projectrc` file inside the new project directory:
```json
{
  "name": "${project_name}",
  "created": "${current_date}",
  "type": "project",
  "status": "active",
  "owner": "",
  "tags": []
}
```
8. Create an initial `README.md` (or `Overview.md` if preferred) to gather project information:
```markdown
# ${project_name}

**Created**: ${current_date}
**Status**: Active

## 🎯 Objectives
- [List project goals here]

## 📝 Description
${project_description}

## 🔗 Resources
- 

## ✅ Todo
- [ ] 

## 📓 Notes
- 
```
9. Confirm to the user that the project has been created and show the path.
