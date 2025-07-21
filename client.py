import asyncio
import websockets
import sys


async def listen(client_id):
    # 서버의 웹소켓 주소
    uri = f"ws://localhost:8000/ws/{client_id}"

    # 웹소켓 서버에 연결
    async with websockets.connect(uri) as websocket:
        print(f"클라이언트 #{client_id}: 서버에 연결되었습니다.")

        # 메시지 보내는 Task와 받는 Task를 동시에 실행
        send_task = asyncio.create_task(send_message(websocket, client_id))
        receive_task = asyncio.create_task(receive_message(websocket, client_id))

        # 두 Task가 끝날 때까지 대기
        await asyncio.gather(send_task, receive_task)


async def send_message(websocket, client_id):
    """사용자 입력을 받아 서버로 메시지를 보냅니다."""
    while True:
        message = await asyncio.to_thread(input, "")  # 비동기적으로 input 받기
        await websocket.send(message)


async def receive_message(websocket, client_id):
    """서버로부터 메시지를 받아 화면에 출력합니다."""
    async for message in websocket:
        print(f"\n[메시지 수신] {message}\n> ", end="")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python client.py <client_id>")
        sys.exit(1)

    client_id = sys.argv[1]
    try:
        asyncio.run(listen(client_id))
    except KeyboardInterrupt:
        print("\n클라이언트 종료.")