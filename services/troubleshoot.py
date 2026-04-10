import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.health_check import run_health_checks
from services.change_analyzer import get_todays_changes, summarise_changes
from services.ai.ai_interface import call_ai
from services.ai.prompts import TROUBLESHOOT_SYSTEM_PROMPT
from database.db import create_incident

def build_troubleshoot_prompt(results, tickets):
    prompt = "Health Check Results:\n"
    for r in results:
        prompt += f"  {r['asset_name']} | {r['check_type']} | {r['status']} | {r['value']}\n"

    prompt += "\nToday's Change Tickets:\n"
    if tickets:
        for t in tickets:
            prompt += f"  {t[0]} | {t[1]} | CI: {t[3]} | {t[5]} | Risk: {t[6]}\n"
    else:
        prompt += "  No change tickets found today.\n"

    prompt += "\nProvide: 1) Root cause diagnosis 2) Remediation steps"
    return prompt

def troubleshoot(application_id):
    # Run health checks
    results = run_health_checks(application_id)

    if not results:
        return {
            'all_clear': True,
            'results': [],
            'message': 'No assets found for this application.'
        }

    #  Find issues
    issues = [r for r in results if r['status'] in ['WARN', 'FAIL']]

    #  All clear path
    if not issues:
        return {
            'all_clear': True,
            'results': results,
            'message': 'All health checks passed.'
        }

    #  Issues found - auto check changes
    asset_names = list(set([r['asset_name'] for r in results]))
    tickets = get_todays_changes(asset_names)

    #  Build prompt and call AI
    prompt = build_troubleshoot_prompt(results, tickets)
    ai_response = call_ai(TROUBLESHOOT_SYSTEM_PROMPT, prompt)

    return {
        'all_clear': False,
        'results': results,
        'issues': issues,
        'tickets': tickets,
        'ai_diagnosis': ai_response
    }

def raise_incident(application_id, issue_summary, root_cause, priority):
    create_incident(application_id, issue_summary, root_cause, priority)
    return f"Incident raised successfully. Priority: {priority}"