#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动下载 HuggingFace 模型脚本
用于在网络不稳定时手动下载模型文件

Copyright (c) 2026 吕滢

Licensed under the MIT License (Non-Commercial) or Apache License 2.0 (Non-Commercial)
See LICENSE-MIT-NC or LICENSE-APACHE-NC for details.

This software is for NON-COMMERCIAL USE ONLY.
For commercial use, please contact the copyright holder.
"""

import os
import sys

def download_model_using_hf_hub():
    """使用 huggingface_hub 下载模型"""
    try:
        from huggingface_hub import snapshot_download
        print("✅ 找到 huggingface_hub 库")
    except ImportError:
        print("❌ 未找到 huggingface_hub 库")
        print("💡 请先安装: pip install huggingface-hub")
        return False
    
    model_id = "BAAI/bge-small-zh-v1.5"
    
    # 检查是否使用镜像
    use_mirror = input("是否使用国内镜像 (HF-Mirror)? [y/N]: ").strip().lower() == 'y'
    
    if use_mirror:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        print("🌐 使用镜像站点: https://hf-mirror.com")
    
    # 选择下载位置
    print("\n选择下载位置:")
    print("1. 项目目录 (./models/BAAI--bge-small-zh-v1.5)")
    print("2. HuggingFace 默认缓存目录 (~/.cache/huggingface/hub/)")
    
    choice = input("请选择 [1/2] (默认: 2): ").strip() or "2"
    
    if choice == "1":
        local_dir = "./models/BAAI--bge-small-zh-v1.5"
        os.makedirs(os.path.dirname(local_dir), exist_ok=True)
        print(f"📁 下载到: {os.path.abspath(local_dir)}")
    else:
        local_dir = None  # 使用默认缓存目录
        cache_path = os.path.join(
            os.path.expanduser("~"),
            ".cache",
            "huggingface",
            "hub",
            f"models--{model_id.replace('/', '--')}"
        )
        print(f"📁 下载到: {cache_path}")
    
    try:
        print(f"\n📥 开始下载模型: {model_id}")
        print("⏳ 这可能需要几分钟，请耐心等待...")
        
        snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True  # 支持断点续传
        )
        
        print("\n✅ 模型下载完成！")
        if local_dir:
            print(f"📁 模型位置: {os.path.abspath(local_dir)}")
        else:
            print(f"📁 模型位置: {cache_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {str(e)}")
        print("\n💡 建议:")
        print("1. 检查网络连接")
        print("2. 如果使用镜像，确保镜像站点可访问")
        print("3. 可以尝试使用代理")
        return False

def download_model_using_cli():
    """使用 huggingface-cli 下载模型"""
    import subprocess
    
    print("📥 使用 huggingface-cli 下载模型...")
    
    # 检查是否使用镜像
    use_mirror = input("是否使用国内镜像 (HF-Mirror)? [y/N]: ").strip().lower() == 'y'
    
    env = os.environ.copy()
    if use_mirror:
        env['HF_ENDPOINT'] = 'https://hf-mirror.com'
        print("🌐 使用镜像站点: https://hf-mirror.com")
    
    # 选择下载位置
    print("\n选择下载位置:")
    print("1. 项目目录 (./models/BAAI--bge-small-zh-v1.5)")
    print("2. HuggingFace 默认缓存目录")
    
    choice = input("请选择 [1/2] (默认: 2): ").strip() or "2"
    
    cmd = ["huggingface-cli", "download", "BAAI/bge-small-zh-v1.5"]
    
    if choice == "1":
        local_dir = "./models/BAAI--bge-small-zh-v1.5"
        os.makedirs(os.path.dirname(local_dir), exist_ok=True)
        cmd.extend(["--local-dir", local_dir])
        print(f"📁 下载到: {os.path.abspath(local_dir)}")
    else:
        print("📁 下载到 HuggingFace 默认缓存目录")
    
    try:
        print(f"\n📥 开始下载模型...")
        print("⏳ 这可能需要几分钟，请耐心等待...")
        
        result = subprocess.run(cmd, env=env, check=True)
        
        print("\n✅ 模型下载完成！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 下载失败: {str(e)}")
        return False
    except FileNotFoundError:
        print("\n❌ 未找到 huggingface-cli")
        print("💡 请先安装: pip install huggingface-hub")
        return False

def main():
    print("=" * 60)
    print("🤖 HuggingFace 模型下载工具")
    print("=" * 60)
    print("\n模型: BAAI/bge-small-zh-v1.5")
    print("大小: 约 130 MB")
    print("用途: 中文文本嵌入（向量化）")
    print("\n" + "=" * 60)
    
    print("\n选择下载方式:")
    print("1. 使用 Python 库 (huggingface_hub) - 推荐")
    print("2. 使用命令行工具 (huggingface-cli)")
    
    choice = input("\n请选择 [1/2] (默认: 1): ").strip() or "1"
    
    if choice == "2":
        success = download_model_using_cli()
    else:
        success = download_model_using_hf_hub()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 下载完成！现在可以运行程序了。")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 下载失败，请查看错误信息并重试。")
        print("💡 更多帮助请查看 MODEL_DOWNLOAD_GUIDE.md")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()

