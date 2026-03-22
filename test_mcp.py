import asyncio
from dia.tools.find_inspo import find_inspo

async def main():
    print("Fetching inspiration...")
    result = await find_inspo("login page saas UI", limit=2)
    print("Result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
