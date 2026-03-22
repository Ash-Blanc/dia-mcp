import os
import asyncio
import json

# Manually load the .env file BEFORE importing tinyfish!
try:
    with open("/home/yash/dev/dia-mcp/.env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key] = val
except Exception as e:
    print(f"Warning: could not process .env manually: {e}")

# Now import the tinyfish client (which grabs the OS env variables we just set)
from dia.clients import tinyfish as tf

async def test_mobbin_login():
    print("Testing Mobbin Login via TinyFish...")
    print(f"Using TinyFish API Key: {os.environ.get('TINYFISH_API_KEY', '')[:10]}...")
    
    goal_query = (
        'Click on the login or sign-in button if you are not already on the login page. '
        'Enter the email address "retidov101@pazard.com" into the email input field. '
        'Enter the password "#9+_!)xhQ?:Kr3D" into the password input field. '
        'Click the login or submit button to authenticate. '
        'Wait for the login process to complete and confirm you are on the authenticated dashboard.'
    )
    
    try:
        # We use run_agent directly here to get detailed output
        result = await tf.run_agent(
            url="https://mobbin.com",
            goal=goal_query,
            stealth=True,
            timeout=300,
            max_steps=12 # Give it enough steps to navigate modal and login
        )
        print("\n=== LOGIN RESULT ===")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print("\n=== LOGIN FAILED ===")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mobbin_login())
