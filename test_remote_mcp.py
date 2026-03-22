import os
import asyncio
import json

# Ensure `.env` is loaded so we can test "WITH our API keys"
try:
    with open("/home/yash/dev/dia-mcp/.env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key] = val
except Exception as e:
    pass

from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def run_tests():
    url = "https://trydia-mcp.onrender.com/sse"
    print(f"Connecting to Remote MCP Server: {url}")
    
    async with sse_client(url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # --- TEST 1: WITHOUT API KEYS ---
            print("\n----- TEST 1: WITHOUT API KEYS -----")
            print("Calling `find_inspo` WITHOUT providing any keys...")
            try:
                res1 = await session.call_tool("find_inspo", arguments={
                    "query": "luxury watch landing page",
                    "limit": 1
                })
                # It should return `{ "total_results": 0 }` gracefully since APIs will block it
                data1 = json.loads(res1.content[0].text)
                print(f"Success! Server gracefully handled missing keys. Total results returned: {data1.get('total_results')}")
            except Exception as e:
                print(f"Error without keys: {e}")
                
            # --- TEST 2: WITH OUR API KEYS ---
            print("\n----- TEST 2: WITH OUR API KEYS AND MOBBIN CREDENTIALS -----")
            fc_key = os.environ.get("FIRECRAWL_API_KEY", "fc-missing")
            tf_key = os.environ.get("TINYFISH_API_KEY", "tf-missing")
            
            print(f"Calling `find_inspo` WITH your Firecrawl and Tinyfish keys...")
            try:
                res2 = await session.call_tool("find_inspo", arguments={
                    "query": "luxury watch landing page",
                    "firecrawl_api_key": fc_key,
                    "tinyfish_api_key": tf_key,
                    "mobbin_login_email": "retidov101@pazard.com",
                    "mobbin_login_password": "#9+_!)xhQ?:Kr3D",
                    "limit": 2
                })
                data2 = json.loads(res2.content[0].text)
                print(f"It worked! Total results returned: {data2.get('total_results')}")
                if data2.get('total_results') > 0:
                    print(f"First result source: {data2['inspiration_board'][0].get('source_platform')}")
            except Exception as e:
                print(f"Error with keys: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())
