# consent.py

from typing import List

# List of all the scopes supported
SUPPORTED_SCOPES = [
    "agent.identity.verify",
    "custom.user.nutrition_profile",
    "custom.user.inventory_access",
    "custom.user.meal_order"
]

# Stores user consent; in production, use DB not dict!
USER_CONSENT = {}  # {user_id: [scopes]}

def request_consent(user_id: str, requested_scopes: List[str]) -> List[str]:
    """Simulate asking user for consent and storing it."""
    # In production, trigger real UI/consent flow.
    granted = [scope for scope in requested_scopes if scope in SUPPORTED_SCOPES]
    USER_CONSENT[user_id] = granted
    return granted

def check_consent(user_id: str, required_scope: str) -> bool:
    """Check if user has granted required scope."""
    return required_scope in USER_CONSENT.get(user_id, [])

def revoke_consent(user_id: str, scope: str):
    """Remove a scope from a user."""
    scopes = USER_CONSENT.get(user_id, [])
    if scope in scopes:
        scopes.remove(scope)
        USER_CONSENT[user_id] = scopes