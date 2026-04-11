import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from services.ai.prompts import TROUBLESHOOT_SYSTEM_PROMPT, CHANGE_SUMMARY_SYSTEM_PROMPT

def call_ai(system_prompt, user_prompt):
    """
    Mock AI service - returns hardcoded realistic responses.
    No API key needed. Swap to real_ai.py after key arrives.
    """

    user_prompt_lower = user_prompt.lower()

    # Troubleshoot response
    if 'troubleshoot' in user_prompt_lower or 'health' in user_prompt_lower:
        if 'warn' in user_prompt_lower or 'fail' in user_prompt_lower:
            return """
DIAGNOSIS:
One or more assets are showing elevated metrics. Based on the health check results and today's change tickets, the most likely cause is a recent patch or config change applied to the affected server. Elevated CPU or disk usage after a patch is a common post-change symptom.

REMEDIATION:
- Verify the patch or change completed successfully on the affected asset
- Clear any temporary patch staging files to free up disk space
- Restart the affected service if it shows as stopped
- Monitor CPU and memory for 30 minutes post-change
- If issue persists, rollback the change using the change ticket reference
- Raise an incident ticket if SLA breach is likely
"""
        else:
            return """
DIAGNOSIS:
All health checks have passed. All assets are operating within normal parameters. No issues detected.

REMEDIATION:
- No immediate action required
- Continue standard monitoring schedule
- Review today's change tickets as a precaution
"""

    # Change ticket summary response
    if 'change' in user_prompt_lower or 'ticket' in user_prompt_lower:
        return """
CHANGE SUMMARY:
One or more change tickets are active today affecting your application assets. Key changes include patching and configuration updates. Medium risk changes are in progress â€” monitor affected assets closely for the next 2 hours post-change window.
"""

    # Default response
    return """
I can help you with:
- Health checks - type 'Run health check for [Application Name]'
- Troubleshooting - type 'Troubleshoot [Application Name]'
- Change analysis - type 'Any changes affecting [Application Name] today?'
"""