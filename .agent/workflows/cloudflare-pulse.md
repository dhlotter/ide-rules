---
description: Get a quick snapshot of traffic and security for your Cloudflare domains.
---

1.  **List zones** to see available domains:
    ```bash
    ".agent/skills/cloudflare-manager/venv/bin/python" \
      ".agent/skills/cloudflare-manager/scripts/dns_list.py"
    ```

2.  **Traffic Snapshot**:
    ```bash
    ".agent/skills/cloudflare-manager/venv/bin/python" \
      ".agent/skills/cloudflare-manager/scripts/analytics_summary.py" --domain <DOMAIN>
    ```

3.  **Security Insights**:
    ```bash
    ".agent/skills/cloudflare-manager/venv/bin/python" \
      ".agent/skills/cloudflare-manager/scripts/security_insights.py"
    ```

4.  **Speed Observatory**:
    ```bash
    ".agent/skills/cloudflare-manager/venv/bin/python" \
      ".agent/skills/cloudflare-manager/scripts/speed_observatory.py" --domain <DOMAIN>
    ```

5.  **Review stats**: Check for spikes in traffic, WAF blocks, performance scores, and security recommendations.
