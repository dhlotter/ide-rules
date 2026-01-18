---
description: Archive a project from 20-Projects to 99-System/Archive/Projects
---

1. List the contents of `/Users/dhlotter/My Drive/obsidian/easyentropy/20-Projects` to help the user identify the project to archive.
2. Ask the user for the name/path of the project folder they want to archive.
3. If the project folder name contains spaces, replace them with dashes (`-`). Rename the folder locally in its current location first if necessary.
4. Check if a `.projectrc` file exists in the project folder. If it does, update the `"status"` field to `"archived"`.
// turbo
5. Move the project folder from `/Users/dhlotter/My Drive/obsidian/easyentropy/20-Projects/` to `/Users/dhlotter/My Drive/obsidian/easyentropy/99-System/Archive/Projects/`.
6. Confirm the archive is complete and provide the new path.
