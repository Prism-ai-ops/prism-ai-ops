import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.db import get_todays_change_tickets
from services.ai.ai_interface import call_ai
from services.ai.prompts import CHANGE_SUMMARY_SYSTEM_PROMPT

def get_todays_changes(asset_names):
    """
    Get today's change tickets matching the given asset names.
    """
    if not asset_names:
        return []
    tickets = get_todays_change_tickets(asset_names)
    return tickets

def summarise_changes(tickets):
    """
    Use AI to summarise the change tickets.
    """
    if not tickets:
        return "No change tickets found for this application today."

    prompt = "Today's Change Tickets:\n"
    for t in tickets:
        prompt += f"  Ticket: {t[0]} | Title: {t[1]} | CI: {t[3]} | Type: {t[4]} | Status: {t[6]}\n"

    summary = call_ai(CHANGE_SUMMARY_SYSTEM_PROMPT, prompt)
    return summary

def analyze_changes(application_id, asset_names):
    """
    Full change analysis flow.
    """
    tickets = get_todays_changes(asset_names)
    summary = summarise_changes(tickets)
    return {
        'tickets': tickets,
        'summary': summary
    }