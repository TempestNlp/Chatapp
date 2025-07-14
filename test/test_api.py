import httpx
import asyncio
import json

async def test_chat_stream():
    prompt = "用中文回答：1+1等于几？"
    model = "deepsex"
    
    print(f"发送请求: {prompt}")
    print("等待响应...\n")
    
    # 关键修改：使用stream=True发起请求
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            async with client.stream(
                "POST",
                "http://localhost:8000/api/chat",
                json={"prompt": prompt, "model": model},
                timeout=None
            ) as response:
                print("实时流式输出:")
                full_response = ""
                
                # 关键修改：直接处理原始字节流
                buffer = b""
                async for chunk in response.aiter_bytes():
                    buffer += chunk
                    try:
                        # 尝试分割并处理完整的JSON行
                        lines = buffer.split(b'\n')
                        for line in lines[:-1]:  # 最后一行可能不完整
                            line = line.strip()
                            if line:
                                data = json.loads(line.decode('utf-8'))
                                if 'response' in data and data['response']:
                                    print(data['response'], end='', flush=True)
                                    full_response += data['response']
                        buffer = lines[-1]  # 保留不完整的部分
                    except json.JSONDecodeError:
                        continue  # 等待更多数据
                    except Exception as e:
                        print(f"\n处理错误: {e}")
                
                # 处理最后剩余的数据
                if buffer.strip():
                    try:
                        data = json.loads(buffer.decode('utf-8'))
                        if 'response' in data and data['response']:
                            print(data['response'], end='', flush=True)
                            full_response += data['response']
                    except json.JSONDecodeError:
                        pass
                
                print(f"\n\n=== 完整回答 ===")
                print(full_response)
                
        except httpx.ConnectError:
            print("无法连接到服务器，请确保后端服务正在运行")
        except Exception as e:
            print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_chat_stream())