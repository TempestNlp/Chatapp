from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx
import logging
import asyncio
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(
        limits=httpx.Limits(
            max_connections=2,  # 减少并发连接数
            max_keepalive_connections=1
        )
    )
    yield
    await app.state.client.aclose()

app = FastAPI(lifespan=lifespan)
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（生产环境应限制）
    allow_methods=["*"],  # 允许所有方法（包括 OPTIONS）
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/api/models")
async def get_models():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:11434/api/tags",
                timeout=5.0  # 添加超时
            )
            response.raise_for_status()  # 自动处理 4XX/5XX 错误
            return response.json()
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not running. Please start it with 'ollama serve'"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama returned error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        model = data.get("model", "deepsex")
        
        async def generate():
            try:
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        "POST",
                        "http://localhost:11434/api/generate",
                        json={
                            "model": model,
                            "prompt": prompt,
                            "stream": True
                        },
                        timeout=None  # 完全禁用超时
                    ) as response:
                        async for chunk in response.aiter_bytes():
                            yield chunk
                            await asyncio.sleep(0.01)  # 降低传输速度
            except Exception as e:
                logger.error(f"流式传输错误: {str(e)}")
                yield b'{"error": "stream interrupted"}'

        return StreamingResponse(
            generate(),
            media_type="application/json"
        )

    except Exception as e:
        logger.error(f"请求处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        workers=1,  # 单工作进程
        timeout_keep_alive=300  # 保持长连接
    )