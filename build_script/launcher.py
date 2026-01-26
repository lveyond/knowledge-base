#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动器脚本 - 用于启动Streamlit应用并自动打开浏览器
"""
import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    """主函数"""
    # 获取脚本所在目录
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe
        app_dir = Path(sys.executable).parent
    else:
        # 如果是Python脚本
        app_dir = Path(__file__).parent
    
    # 切换到应用目录
    os.chdir(app_dir)
    
    # 主程序文件路径
    main_file = app_dir / "knowledge_base_deepseek.py"
    
    if not main_file.exists():
        print(f"错误: 找不到主程序文件 {main_file}")
        input("按回车键退出...")
        sys.exit(1)
    
    print("=" * 50)
    print("智能知识库系统")
    print("=" * 50)
    print()
    print("正在启动应用...")
    print("应用启动后会自动在浏览器中打开")
    print("如果没有自动打开，请访问: http://localhost:8501")
    print()
    print("按 Ctrl+C 可以停止应用")
    print("=" * 50)
    print()
    
    # 启动Streamlit
    try:
        # 等待几秒后打开浏览器
        def open_browser():
            time.sleep(3)  # 等待Streamlit启动
            webbrowser.open("http://localhost:8501")
        
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 运行Streamlit
        # 如果是打包后的exe，使用sys.executable；否则使用python -m streamlit
        if getattr(sys, 'frozen', False):
            # 打包后的exe，直接调用streamlit模块
            import streamlit.web.cli as stcli
            sys.argv = ["streamlit", "run", str(main_file)]
            stcli.main()
        else:
            # 开发环境，使用subprocess
            cmd = [sys.executable, "-m", "streamlit", "run", str(main_file)]
            subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n正在关闭应用...")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
