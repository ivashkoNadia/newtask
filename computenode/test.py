# from requests import post
#
# url = "http://192.168.1.6/compute"
# post(url, json={"user_id": 1, "method": "gauss", "input_data": [0, 1, 2]})

import httpx
from asyncio import sleep


server_url = "http://192.168.0.100"  # Замініть це на реальний URL сервера


async def test_compute_endpoint():
    user_id = 1

    input_data = [[1, 2, 3, 4]]
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{server_url}/createTask",
            json={"user_id": user_id, "input_data": input_data},
        )
        response_data = response.json()
        print("task created", response_data)
        return
        await sleep(30)
        task_id = response_data["task_id"]
        print("canceling", task_id)
        response = await client.post(
            f"{server_url}/cancel_task",
            json={"task_id": task_id}
        )
        print(response.json())


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_compute_endpoint())