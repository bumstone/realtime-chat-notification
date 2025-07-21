from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

# 연결된 클라이언트들을 관리
class ConnectionManager:
    def __init__(self):
        # 활성화된 연결(WebSocket 객체)을 저장할 리스트
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # 클라이언트의 연결을 수락
        await websocket.accept()
        # 활성화된 연결 리스트에 추가
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # 활성화된 연결 리스트에서 제거
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # 특정 클라이언트에게 개인 메시지 전송
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # 연결된 모든 클라이언트에게 메시지 전송 (브로드캐스팅)
        for connection in self.active_connections:
            await connection.send_text(message)

# FastAPI 앱 생성 및 ConnectionManager 인스턴스 생성
app = FastAPI()
manager = ConnectionManager()


# 클라이언트와 웹소켓 통신 엔드포인트
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # 클라이언트 연결
    await manager.connect(websocket)
    # 연결된 모든 클라이언트에게 새로운 사용자 입장 알림
    await manager.broadcast(f"클라이언트 #{client_id} 님이 채팅에 참여했습니다.")

    try:
        # 클라이언트로부터 메시지를 계속 받기 위해 무한 루프
        while True:
            # 클라이언트로부터 메시지 수신 대기
            data = await websocket.receive_text()
            # 받은 메시지를 다른 모든 클라이언트에게 전송
            await manager.broadcast(f"클라이언트 #{client_id}: {data}")

    except WebSocketDisconnect:
        # 클라이언트 연결이 끊어졌을 때
        manager.disconnect(websocket)
        # 연결이 끊어진 클라이언트를 모든 클라이언트에게 알림
        await manager.broadcast(f"클라이언트 #{client_id} 님이 채팅을 나갔습니다.")


# 특정 사용자에게 알림 전송 HTTP 엔드포인트
@app.post("/notify/{client_id}")
async def notify_client(client_id: int, message: str):
    # 현재 연결된 모든 웹소켓을 순회
    for connection in manager.active_connections:
        # URL의 client_id와 웹소켓의 client_id가 일치하는지 확인
        # (실제 프로덕션에서는 웹소켓 연결 시 사용자 정보를 저장하는 더 좋은 방법 사용)
        if connection.path_params['client_id'] == str(client_id):
            await manager.send_personal_message(f"서버 알림: {message}", connection)
            return {"message": f"클라이언트 #{client_id}에게 알림 전송 성공"}

    return {"message": f"클라이언트 #{client_id}를 찾을 수 없거나 연결되지 않았습니다."}