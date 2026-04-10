import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname((__file__))))
import config


def call_ai(system_prompt, user_prompt):
    """
    Main AI entry point.
    Automatically uses mock or real AI based on config.AI_PROVIDER.
    """

    if config.AI_PROVIDER == "anthropic":
        from services.ai.real_ai import call_ai as real_call
        return real_call(system_prompt, user_prompt)
    else:
        from services.ai.mock_ai import call_ai as mock_call
        return mock_call(system_prompt, user_prompt)