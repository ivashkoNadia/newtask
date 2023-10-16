#server_url = "http://192.168.0.100"  # Замініть це на реальний URL сервера

import httpx

async def test_registration():
    url = "http://192.168.0.100/registration"  # Замініть це на фактичну URL вашого API
    json_data = {
        "email": "example@email.com",
        "password": "password123"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data)

    if response.status_code == 200:
        print("Registration successful")
        print(response.json())
    else:
        print("Registration failed")
        print(f"Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_registration())
