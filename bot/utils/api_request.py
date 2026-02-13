from aiohttp import ClientSession

async def create_searches_task(link: str, user_id):
    async with ClientSession() as session:
        await session.post(
            'http://localhost:8000/search-url',
            json={'search_link': link, 'user_id': str(user_id)}
        )