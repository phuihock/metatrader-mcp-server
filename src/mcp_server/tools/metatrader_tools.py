import random

# The FastMCP server instance will import this module and register tools.
def get_balance() -> int:
    """
    Get user's account balance.
    
    Returns:
        int: Current account balance.
    """
    return random.randint(100_000, 400_000)
