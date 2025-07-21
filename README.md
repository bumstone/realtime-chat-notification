## WebSocket을 적용한 시스템 구조

- **연결 관리자 (Connection Manager)**
    - 기능: 모든 웹소켓 연결 관리
    - 역할: 연결 상태 추적 및 메시지 전달
    - 주요 메서드:
        - `connect`: 신규 클라이언트 연결 추가
        - `disconnect`: 연결 종료된 클라이언트 제거
        - `send_personal_message`: 특정 클라이언트에 메시지 전송
        - `broadcast`: 모든 클라이언트에 동시 메시지 전송
- **웹소켓 엔드포인트 (WebSocket Endpoint)**
    - 정의: FastAPI에서 웹소켓 연결 요청 처리 경로
    - 구현: `@app.websocket("/ws/{client_id}")` 데코레이터 사용
    - 역할: 클라이언트와 양방향 통신 채널 설정

---

## 필요한 라이브러리 설치

```bash
pip install fastapi "uvicorn[standard]" websockets

pip install websockets(가상환경 내) 
```

## 서버 실행

```bash
uvicorn main:app --reload
```

[http://127.0.0.1:8000](http://127.0.0.1:8000/) 에서 서버 실행

---

## Test -  터미널별 채팅 시스템

터미널별 사용자 접속

```python
python client.py 1
```

`클라이언트 #1: 서버에 연결되었습니다.`

`[메시지 수신] 클라이언트 #2 님이 채팅에 참여했습니다.`

Hello →

`[메시지 수신] 클라이언트 #2: world!`

```python
python client.py 2
```

`클라이언트 #2: 서버에 연결되었습니다.`

`[메시지 수신] 클라이언트 #1: Hello`

world! →

### Test - 알림시스템

새 터미널3 생성 후 명령 (/notify/{client_id})

```python
curl -X POST "http://localhost:8000/notify/1?message=서버에서 보낸 중요한 공지입니다!" 
```

**사용자 1의 터미널** 화면에서만 `[메시지 수신] 서버 알림: 서버에서 보낸 중요한 공지입니다!` 라는 알림
