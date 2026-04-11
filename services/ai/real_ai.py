import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname((__file__))))
import config


def call_ai(system_prompt, user_prompt):
    """
    Real AI service - uses Anthropic claude API.
    Only Activated when AI_PROVIDER = 'anthropic' in config.py
    """

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        message = client.message.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=1024,
            system=system_prompt,
            message=[
                {
                    "role": "user", "content": user_prompt
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"AI ERROR: {str(e)}"