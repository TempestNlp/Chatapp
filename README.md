
## 项目介绍
本项目是与大模型对话的后端应用，部署后可对外提供大模型对话、查询等 API，依赖 Ollama 服务进行模型推理。


## 环境依赖
1. Python 版本：3.10.9  
   - 安装建议：通过 [Python 官网](https://www.python.org/downloads/) 或 Anaconda 安装对应版本。

2. Python 依赖安装：  
   ```bash
   pip install -r requirements.txt

3. Ollama 版本：0.9.6
  -安装方式：参考 Ollama 官方文档 下载对应系统的安装包。
  -启动服务：安装后执行 ollama serve 启动服务（默认监听 http://localhost:11434）。
  -验证安装：运行 ollama --version 确认版本是否正确。

## 项目描述
- `main.py`：项目主文件，运行后对外提供大模型对话、查询等 API，默认监听 8000 端口。  
- `test_api.py`：API 测试脚本，用于验证项目提供的接口是否正常。  
- `test_ollma.py`：Ollama 服务测试脚本，用于检查本地 Ollama 服务是否可用。  
- `requirements.txt`：Python 依赖列表，通过 `pip install -r` 安装。  
- `.env.example`：环境变量模板，**运行前必须配置**：  
  1. 复制 `.env.example` 为 `.env`；  
  2. 填写必要配置（如 `OLLAMA_BASE_URL` 等，具体见文件内注释）。

## 运行项目
1. 确保 Ollama 服务已启动（见“环境依赖”步骤）。  
2. 配置 `.env` 文件（见上文说明）。  
3. 启动项目：  
   ```bash
   python main.py
