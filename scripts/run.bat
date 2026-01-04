@echo off
cd /d "%~dp0\.."
echo 正在启动智能知识库系统...
echo.
echo 请确保已安装所有依赖: pip install -r requirements.txt
echo.
streamlit run knowledge_base_deepseek.py
pause

