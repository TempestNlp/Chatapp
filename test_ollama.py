import requests
import json

def test_ollama():
    # 测试生成（流式模式）
    print("\n=== 流式生成测试 ===")
    try:
        data = {
            "model": "deepsex:latest",
            "prompt": "用中文回答：1+1等于几？",
            "stream": True  # 启用流式
        }
        
        with requests.post("http://localhost:11434/api/generate", 
                         json=data,
                         stream=True) as response:
            
            print("实时流式输出：")
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        print(chunk['response'], end='', flush=True)
                        full_response += chunk['response']
            
            print(f"\n\n=== 完整响应 ===")
            print(full_response)
            
    except Exception as e:
        print(f"\n发生错误: {e}")

if __name__ == "__main__":
    test_ollama()