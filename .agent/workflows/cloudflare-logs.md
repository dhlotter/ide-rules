---
description: Monitor and tail live logs for Cloudflare Pages deployments.
---

1.  **Find your project name** (if not known):
    ```bash
    wrangler pages project list
    ```

2.  **List recent deployments** to get the deployment ID or just check status:
    ```bash
    wrangler pages deployment list --project-name <PROJECT_NAME>
    ```

3.  **Tail live logs** for the latest deployment:
    ```bash
    wrangler pages deployment tail --project-name <PROJECT_NAME>
    ```

    *Tip: You can filter by environment (production/preview) using `--environment preview`.*

4.  **Check for errors**: Look for 5xx status codes or uncaught exceptions in the streamed logs.
