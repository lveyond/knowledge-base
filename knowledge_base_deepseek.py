import streamlit as st
import os
import glob
from typing import List, Dict, Any, Optional
import tempfile
from pathlib import Path
import json
from datetime import datetime
import base64
import hashlib

# API Key 管理模块
CONFIG_FILE = os.path.join(".", ".deepseek_config.json")

def encode_api_key(api_key: str) -> str:
    """简单的编码（Base64），不是真正的加密，但可以避免完全明文"""
    if not api_key:
        return ""
    # 使用 Base64 编码
    encoded = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
    return encoded

def decode_api_key(encoded_key: str) -> str:
    """解码 API key"""
    if not encoded_key:
        return ""
    try:
        decoded = base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')
        return decoded
    except Exception:
        return ""

def save_api_key(api_key: str, show_error: bool = True) -> bool:
    """保存 API key 到本地配置文件"""
    try:
        config = {
            "api_key": encode_api_key(api_key),
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        os.makedirs(os.path.dirname(CONFIG_FILE) if os.path.dirname(CONFIG_FILE) else ".", exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        if show_error and 'st' in globals():
            st.error(f"保存 API key 失败: {str(e)}")
        return False

def load_api_key() -> Optional[str]:
    """从本地配置文件加载 API key"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = decode_api_key(config.get("api_key", ""))
                if api_key:
                    return api_key
    except Exception as e:
        # 静默失败，如果文件损坏或不存在，返回 None
        pass
    return None

def delete_api_key(show_error: bool = True) -> bool:
    """删除本地保存的 API key"""
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            return True
        return False
    except Exception as e:
        if show_error and 'st' in globals():
            st.error(f"删除 API key 失败: {str(e)}")
        return False

# 文件读取模块
def read_text_file(file_path):
    """读取txt文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_docx_file(file_path):
    """读取Word文档"""
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except ImportError:
        return "请安装python-docx: pip install python-docx"

def read_pdf_file(file_path):
    """读取PDF文件"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"PDF读取失败: {str(e)}"

def read_excel_file(file_path):
    """读取Excel文件"""
    try:
        import pandas as pd
        excel_content = {}
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            excel_content[sheet_name] = df.to_string()
        return excel_content
    except ImportError:
        return {"错误": "请安装pandas和openpyxl"}

def process_folder(folder_path: str) -> Dict[str, Any]:
    """处理文件夹中的所有文件"""
    all_docs = {}
    
    # 支持的文件类型
    file_patterns = {
        '*.txt': ('txt', read_text_file),
        '*.docx': ('docx', read_docx_file),
        '*.pdf': ('pdf', read_pdf_file),
        '*.xlsx': ('excel', read_excel_file),
        '*.xls': ('excel', read_excel_file),
    }
    
    for pattern, (file_type, reader_func) in file_patterns.items():
        for file_path in glob.glob(os.path.join(folder_path, pattern)):
            file_name = os.path.basename(file_path)
            try:
                content = reader_func(file_path)
                all_docs[file_name] = {
                    'path': file_path,
                    'content': content,
                    'type': file_type,
                    'size': os.path.getsize(file_path)
                }
            except Exception as e:
                all_docs[file_name] = {
                    'path': file_path,
                    'content': f"读取失败: {str(e)}",
                    'type': 'error',
                    'size': 0
                }
    
    return all_docs

# 本地向量数据库模块（不需要API密钥）
def get_model_path(model_name: str = "BAAI/bge-small-zh-v1.5") -> str:
    """获取模型路径，优先使用本地路径
    
    Args:
        model_name: HuggingFace 模型名称或本地路径
    
    Returns:
        模型路径（本地路径如果存在，否则返回模型名称）
    """
    import os
    
    try:
        # 如果已经是本地路径且存在，直接返回
        if os.path.exists(model_name) and os.path.isdir(model_name):
            return model_name
        
        # 检查 HuggingFace 缓存目录
        cache_dir = os.path.join(
            os.path.expanduser("~"),
            ".cache",
            "huggingface",
            "hub"
        )
        
        # 将模型名称转换为缓存目录格式（BAAI/bge-small-zh-v1.5 -> models--BAAI--bge-small-zh-v1.5）
        cache_model_name = f"models--{model_name.replace('/', '--')}"
        cache_path = os.path.join(cache_dir, cache_model_name)
        
        # 查找 snapshots 目录下的最新版本
        if os.path.exists(cache_path):
            snapshots_dir = os.path.join(cache_path, "snapshots")
            if os.path.exists(snapshots_dir):
                try:
                    # 获取所有快照版本
                    snapshots = [d for d in os.listdir(snapshots_dir) 
                                if os.path.isdir(os.path.join(snapshots_dir, d))]
                    if snapshots:
                        # 使用最新的快照
                        latest_snapshot = sorted(snapshots)[-1]
                        local_path = os.path.join(snapshots_dir, latest_snapshot)
                        if os.path.exists(local_path):
                            return local_path
                except (OSError, PermissionError):
                    pass  # 忽略访问错误，继续检查其他路径
        
        # 检查项目目录下的 models 文件夹
        project_model_path = os.path.join(".", "models", model_name.replace("/", "--"))
        if os.path.exists(project_model_path):
            return project_model_path
    except Exception:
        pass  # 如果出现任何错误，返回原始模型名称
    
    # 如果都不存在，返回原始模型名称（会触发下载）
    return model_name

def check_db_corrupted(db_path: str) -> bool:
    """检测向量数据库是否损坏（特别是 schema 兼容性问题）
    
    Args:
        db_path: 向量数据库路径
    
    Returns:
        True 如果数据库损坏，False 如果正常或不存在
    """
    if not os.path.exists(db_path):
        return False
    
    try:
        # 尝试加载数据库来检测是否损坏
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
        
        try:
            from langchain_chroma import Chroma
        except ImportError:
            from langchain_community.vectorstores import Chroma
        
        # 初始化嵌入模型
        model_path = get_model_path("BAAI/bge-small-zh-v1.5")
        embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # 尝试加载向量数据库
        vectorstore = Chroma(
            persist_directory=db_path,
            embedding_function=embeddings
        )
        
        # 尝试访问数据库（如果 schema 错误会在这里失败）
        _ = len(vectorstore)
        return False  # 数据库正常
    except Exception as e:
        error_msg = str(e).lower()
        # 检测常见的数据库错误
        is_corrupted = (
            "no such column" in error_msg or
            "collections.topic" in error_msg or
            "hnsw" in error_msg or
            "index" in error_msg or
            "compaction" in error_msg or
            "segment" in error_msg or
            "schema" in error_msg or
            "sqlite" in error_msg
        )
        if is_corrupted:
            print(f"⚠️ 检测到数据库损坏: {str(e)}")
        return is_corrupted

def cleanup_corrupted_db(db_path: str, force: bool = True):
    """彻底清理损坏的向量数据库目录
    
    Args:
        db_path: 向量数据库路径
        force: 是否强制清理（包括多次尝试和延迟）
    
    Returns:
        bool: 是否成功清理
    """
    import shutil
    import time
    
    if not os.path.exists(db_path):
        return True
    
    if force:
        # 强制清理模式：多次尝试，确保彻底删除
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                # 先尝试正常删除
                if os.path.exists(db_path):
                    shutil.rmtree(db_path, ignore_errors=False)
                
                # 等待一下，确保文件系统更新
                time.sleep(0.5)
                
                # 验证是否删除成功
                if not os.path.exists(db_path):
                    print(f"✅ 已彻底清理损坏的向量数据库目录: {db_path}")
                    return True
                    
            except PermissionError as pe:
                # Windows 上可能有文件被锁定，等待后重试
                if attempt < max_attempts - 1:
                    print(f"⚠️ 文件被锁定，等待后重试 ({attempt + 1}/{max_attempts})...")
                    time.sleep(1)
                    continue
                else:
                    print(f"❌ 清理失败（文件被锁定）: {str(pe)}")
                    print(f"   请手动删除目录: {db_path}")
                    return False
            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"⚠️ 清理失败，重试 ({attempt + 1}/{max_attempts}): {str(e)}")
                    time.sleep(0.5)
                    continue
                else:
                    print(f"❌ 清理失败: {str(e)}")
                    print(f"   请手动删除目录: {db_path}")
                    return False
        
        # 如果多次尝试后仍然存在，尝试使用 ignore_errors
        if os.path.exists(db_path):
            try:
                shutil.rmtree(db_path, ignore_errors=True)
                time.sleep(0.5)
                if not os.path.exists(db_path):
                    print(f"✅ 已强制清理数据库目录: {db_path}")
                    return True
            except Exception:
                pass
        
        # 最后尝试：重命名目录（如果无法删除）
        if os.path.exists(db_path):
            try:
                import tempfile
                temp_name = db_path + "_deleted_" + str(int(time.time()))
                os.rename(db_path, temp_name)
                print(f"⚠️ 无法删除目录，已重命名为: {temp_name}")
                print(f"   请稍后手动删除")
                return True
            except Exception as e:
                print(f"❌ 无法清理目录: {str(e)}")
                print(f"   请手动删除: {db_path}")
                return False
        
        return False
    else:
        # 简单清理模式
        try:
            if os.path.exists(db_path):
                shutil.rmtree(db_path)
                print(f"✅ 已清理数据库目录: {db_path}")
                return True
        except Exception as e:
            print(f"⚠️ 清理失败: {str(e)}")
            return False
    
    return False

def get_vector_db_path(folder_path: str) -> str:
    """根据文件夹路径生成唯一的向量数据库目录路径
    
    Args:
        folder_path: 文件夹路径
    
    Returns:
        向量数据库目录路径
    """
    if not folder_path:
        # 上传文件时没有文件夹路径，使用默认路径
        return "./chroma_db"
    
    # 使用路径的哈希值创建唯一目录名
    # 规范化路径（统一使用正斜杠，处理大小写）
    normalized_path = os.path.normpath(folder_path).replace('\\', '/')
    path_hash = hashlib.md5(normalized_path.encode('utf-8')).hexdigest()[:12]
    
    # 创建安全的目录名（移除特殊字符）
    safe_folder_name = os.path.basename(normalized_path)
    safe_folder_name = "".join(c for c in safe_folder_name if c.isalnum() or c in (' ', '-', '_'))[:30]
    safe_folder_name = safe_folder_name.strip() or "unknown"
    
    # 组合目录名：文件夹名_哈希值
    db_dir_name = f"{safe_folder_name}_{path_hash}"
    return os.path.join("./chroma_db", db_dir_name)

def load_existing_vector_store(folder_path: str = None, progress_callback=None):
    """加载已有的向量数据库
    
    Args:
        folder_path: 文件夹路径（用于确定向量数据库位置）
        progress_callback: 进度回调函数，接收 (progress, message) 参数
    
    Returns:
        向量数据库对象，如果不存在或加载失败则返回 None
    """
    try:
        # 优先使用新版本的包
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
        
        try:
            from langchain_chroma import Chroma
        except ImportError:
            from langchain_community.vectorstores import Chroma
        
        db_path = get_vector_db_path(folder_path) if folder_path else "./chroma_db"
        
        if not os.path.exists(db_path):
            return None
        
        if progress_callback:
            progress_callback(10, "🔄 正在加载已有向量数据库...")
        
        # 初始化嵌入模型（必须与创建时使用相同的模型）
        # 优先使用本地模型路径，避免网络下载
        model_path = get_model_path("BAAI/bge-small-zh-v1.5")
        embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        if progress_callback:
            progress_callback(50, "🔄 正在加载向量数据库...")
        
        # 从持久化目录加载
        vectorstore = Chroma(
            persist_directory=db_path,
            embedding_function=embeddings
        )
        
        # 验证向量数据库是否可用（尝试获取数量，如果索引损坏会在这里失败）
        try:
            _ = len(vectorstore)  # 这会触发 count() 调用，如果索引损坏会抛出异常
        except Exception as verify_error:
            # 索引文件可能损坏，检测是否是 schema 错误
            error_msg = str(verify_error).lower()
            is_schema_error = (
                "no such column" in error_msg or
                "collections.topic" in error_msg or
                "schema" in error_msg
            )
            
            if is_schema_error:
                # Schema 错误（版本兼容性问题），清理数据库
                if progress_callback:
                    progress_callback(100, "⚠️ 检测到数据库 schema 错误（版本兼容性问题），正在清理...")
                cleanup_corrupted_db(db_path, force=True)
            else:
                # 其他错误（如索引损坏），也清理
                if progress_callback:
                    progress_callback(100, "⚠️ 向量数据库索引可能损坏，将重新创建...")
                cleanup_corrupted_db(db_path, force=True)
            return None
        
        if progress_callback:
            progress_callback(100, "✅ 向量数据库加载完成！")
        
        return vectorstore
    except Exception as e:
        # 加载失败，返回 None
        return None

def calculate_content_hash(content: Any) -> str:
    """计算文档内容的哈希值
    
    Args:
        content: 文档内容（字符串或字典）
    
    Returns:
        内容的 MD5 哈希值
    """
    if isinstance(content, dict):
        # Excel 文件：合并所有工作表内容
        content_str = "\n".join([f"{k}:{v}" for k, v in content.items()])
    else:
        content_str = str(content)
    
    return hashlib.md5(content_str.encode('utf-8')).hexdigest()

def check_docs_changed(docs_dict: Dict[str, Any], folder_path: str) -> bool:
    """检查文档是否发生变化
    
    Args:
        docs_dict: 当前文档字典
        folder_path: 文件夹路径
    
    Returns:
        True 如果文档发生变化，False 如果未变化
    """
    # 创建文档签名文件路径（基于文件夹路径）
    db_path = get_vector_db_path(folder_path)
    signature_file = os.path.join(db_path, ".docs_signature.json")
    
    if not os.path.exists(signature_file):
        return True  # 签名文件不存在，认为文档已变化
    
    try:
        # 读取之前的签名
        with open(signature_file, 'r', encoding='utf-8') as f:
            old_signature = json.load(f)
        
        # 生成当前文档签名
        current_signature = {
            "folder_path": folder_path,
            "file_count": len(docs_dict),
            "files": {}
        }
        
        for filename, data in docs_dict.items():
            file_path = data.get('path', '')
            content = data.get('content', '')
            
            file_info = {
                "size": data.get('size', 0),
                "content_hash": calculate_content_hash(content)  # 使用内容哈希
            }
            
            # 如果文件路径存在且是持久路径（非临时路径），也记录修改时间
            if file_path and os.path.exists(file_path):
                # 检查是否是临时路径（临时路径通常包含 temp 或 tmp）
                is_temp_path = 'temp' in file_path.lower() or 'tmp' in file_path.lower()
                if not is_temp_path:
                    file_info["mtime"] = os.path.getmtime(file_path)
            
            current_signature["files"][filename] = file_info
        
        # 比较签名
        if old_signature.get("folder_path") != current_signature["folder_path"]:
            return True
        
        if old_signature.get("file_count") != current_signature["file_count"]:
            return True
        
        old_files = old_signature.get("files", {})
        current_files = current_signature["files"]
        
        if set(old_files.keys()) != set(current_files.keys()):
            return True
        
        # 检查文件内容哈希（优先）和文件大小/修改时间
        for filename in old_files.keys():
            if filename not in current_files:
                return True
            
            old_info = old_files[filename]
            current_info = current_files[filename]
            
            # 优先使用内容哈希进行比较（最可靠的方法）
            old_hash = old_info.get("content_hash")
            current_hash = current_info.get("content_hash")
            
            # 如果当前有内容哈希，优先使用哈希比较
            if current_hash:
                if old_hash:
                    # 两者都有哈希值，直接比较
                    if old_hash != current_hash:
                        return True
                    # 哈希值相同，认为文档未变化（即使修改时间不同）
                    continue
                else:
                    # 旧签名没有哈希值（可能是旧版本保存的），但当前有
                    # 这种情况下，我们只比较文件大小，不比较修改时间
                    # 因为修改时间可能因为各种原因变化（文件被重新保存、系统时间调整等）
                    # 但文件大小相同通常意味着内容相同（虽然不是100%确定，但概率很高）
                    if old_info.get("size") != current_info.get("size"):
                        return True
                    # 文件大小相同，认为文档未变化（即使修改时间不同）
                    # 签名文件会在保存时更新，添加内容哈希，下次比较会更准确
                    continue
            
            # 如果当前没有内容哈希（不应该发生，但为了兼容性保留）
            # 回退到大小和修改时间比较
            if (old_info.get("size") != current_info.get("size") or 
                (old_info.get("mtime") and current_info.get("mtime") and
                 abs(old_info.get("mtime", 0) - current_info.get("mtime", 0)) > 1)):
                return True
        
        return False  # 文档未变化
    except Exception as e:
        # 读取签名失败，认为文档已变化
        return True

def save_docs_signature(docs_dict: Dict[str, Any], folder_path: str):
    """保存文档签名
    
    Args:
        docs_dict: 文档字典
        folder_path: 文件夹路径
    """
    try:
        db_path = get_vector_db_path(folder_path)
        os.makedirs(db_path, exist_ok=True)
        signature_file = os.path.join(db_path, ".docs_signature.json")
        
        signature = {
            "folder_path": folder_path,
            "file_count": len(docs_dict),
            "files": {},
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for filename, data in docs_dict.items():
            file_path = data.get('path', '')
            content = data.get('content', '')
            
            file_info = {
                "size": data.get('size', 0),
                "content_hash": calculate_content_hash(content)  # 保存内容哈希
            }
            
            # 如果文件路径存在且是持久路径（非临时路径），也记录修改时间
            if file_path and os.path.exists(file_path):
                # 检查是否是临时路径
                is_temp_path = 'temp' in file_path.lower() or 'tmp' in file_path.lower()
                if not is_temp_path:
                    file_info["mtime"] = os.path.getmtime(file_path)
            
            signature["files"][filename] = file_info
        
        with open(signature_file, 'w', encoding='utf-8') as f:
            json.dump(signature, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # 保存签名失败不影响主流程

def create_local_vector_store(docs_dict: Dict[str, Any], progress_callback=None, folder_path: str = None):
    """创建本地向量数据库，使用开源嵌入模型
    
    Args:
        docs_dict: 文档字典
        progress_callback: 进度回调函数，接收 (progress, message) 参数
        folder_path: 文件夹路径（用于签名）
    """
    try:
        # 兼容不同版本的 langchain 导入
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError:
            try:
                from langchain.text_splitter import RecursiveCharacterTextSplitter
            except ImportError:
                from langchain_core.text_splitter import RecursiveCharacterTextSplitter
        
        # 优先使用新版本的包
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
        
        try:
            from langchain_chroma import Chroma
        except ImportError:
            from langchain_community.vectorstores import Chroma
        try:
            from langchain.schema import Document as LangDocument
        except ImportError:
            from langchain_core.documents import Document as LangDocument
        
        # 步骤 0: 在开始处理之前，先检测并清理损坏的数据库目录（避免版本兼容性问题）
        db_path = get_vector_db_path(folder_path) if folder_path else "./chroma_db"
        
        # 检查目录权限（在创建目录之前）
        parent_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else "."
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        if not os.access(parent_dir, os.W_OK):
            raise PermissionError(f"没有写入权限: {parent_dir}")
        
        # 如果数据库目录已存在，先检测是否损坏，然后清理（避免版本兼容性问题）
        if os.path.exists(db_path):
            if progress_callback:
                progress_callback(5, "🔄 检测向量数据库状态...")
            
            # 先检测数据库是否损坏（特别是 schema 兼容性问题）
            is_corrupted = check_db_corrupted(db_path)
            
            if is_corrupted:
                if progress_callback:
                    progress_callback(5, "⚠️ 检测到数据库损坏（可能是版本兼容性问题），正在清理...")
                cleanup_corrupted_db(db_path, force=True)
                import time
                time.sleep(1)  # 等待文件系统更新
            else:
                # 即使检测正常，如果文档变化了，也需要清理重建
                # 这里先不清理，让后续逻辑处理
                pass
        
        # 确保损坏的目录被清理
        if os.path.exists(db_path):
            # 再次尝试清理（防止检测遗漏）
            try:
                # 快速检测：如果目录存在但很小或结构异常，可能是损坏的
                import time
                if progress_callback:
                    progress_callback(5, "🔄 清理旧的向量数据库目录...")
                cleanup_corrupted_db(db_path, force=True)
                time.sleep(0.5)  # 等待文件系统更新
            except Exception:
                pass
        
        # 如果仍然存在，尝试重命名（最后的手段）
        if os.path.exists(db_path):
            import time
            backup_name = db_path + "_backup_" + str(int(time.time()))
            try:
                os.rename(db_path, backup_name)
                print(f"⚠️ 无法删除目录，已重命名为备份: {backup_name}")
            except Exception:
                pass
        
        # 提取文本内容
        if progress_callback:
            progress_callback(15, "🔄 步骤 1/4: 提取文档内容...")
        
        texts = []
        total_files = len(docs_dict)
        for idx, (filename, data) in enumerate(docs_dict.items()):
            content = data['content']
            if isinstance(content, dict):  # Excel文件
                for sheet, sheet_content in content.items():
                    texts.append(f"文件: {filename} | 工作表: {sheet}\n{sheet_content}")
            else:
                texts.append(f"文件: {filename}\n{content}")
            
            if progress_callback and total_files > 0:
                progress = 15 + int((idx + 1) / total_files * 10)
                progress_callback(progress, f"🔄 步骤 1/4: 提取文档内容... ({idx + 1}/{total_files})")
        
        # 分割文本
        if progress_callback:
            progress_callback(30, "🔄 步骤 2/4: 分割文本...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        documents = []
        total_texts = len(texts)
        for i, text in enumerate(texts):
            splits = text_splitter.split_text(text)
            for split in splits:
                documents.append(LangDocument(
                    page_content=split,
                    metadata={"source": list(docs_dict.keys())[i % len(docs_dict)]}
                ))
            
            if progress_callback and total_texts > 0:
                progress = 30 + int((i + 1) / total_texts * 20)
                progress_callback(progress, f"🔄 步骤 2/4: 分割文本... ({i + 1}/{total_texts})")
        
        # 使用本地嵌入模型
        if progress_callback:
            progress_callback(55, "🔄 步骤 3/4: 初始化嵌入模型（首次运行会下载模型，可能需要几分钟）...")
        
        # 优先使用本地模型路径，避免网络下载
        model_path = get_model_path("BAAI/bge-small-zh-v1.5")
        
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name=model_path,  # 中文优化的小模型
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as model_error:
            error_type = type(model_error).__name__
            error_msg = str(model_error)
            raise Exception(f"嵌入模型初始化失败 [{error_type}]: {error_msg}\n\n"
                          f"可能的原因:\n"
                          f"- 模型文件不存在或损坏\n"
                          f"- 网络连接问题（无法下载模型）\n"
                          f"- 模型路径配置错误: {model_path}\n\n"
                          f"解决方案:\n"
                          f"- 检查模型文件是否存在\n"
                          f"- 使用 download_model.py 手动下载模型\n"
                          f"- 检查网络连接") from model_error
        
        if progress_callback:
            progress_callback(70, "🔄 步骤 3/4: 生成向量嵌入（这可能需要几分钟，请耐心等待）...")
        
        # 检查文档是否为空
        if not documents or len(documents) == 0:
            raise ValueError("没有可用的文档内容，无法创建向量数据库。请检查文档是否为空或格式是否正确。")
        
        # 创建向量存储
        if progress_callback:
            progress_callback(85, "🔄 步骤 4/4: 创建向量存储...")
        
        # 确保使用全新的目录（如果目录仍然存在，再次清理）
        if os.path.exists(db_path):
            # 最后一次清理尝试
            cleanup_corrupted_db(db_path, force=True)
            import time
            time.sleep(0.5)
        
        # 确保目录不存在后再创建
        if not os.path.exists(db_path):
            os.makedirs(db_path, exist_ok=True)
        else:
            # 如果仍然存在，尝试重命名
            import time
            backup_name = db_path + "_backup_" + str(int(time.time()))
            try:
                os.rename(db_path, backup_name)
                print(f"⚠️ 无法删除目录，已重命名为备份: {backup_name}")
                os.makedirs(db_path, exist_ok=True)
            except Exception:
                # 如果重命名也失败，尝试强制删除
                cleanup_corrupted_db(db_path, force=True)
                time.sleep(0.5)
                if not os.path.exists(db_path):
                    os.makedirs(db_path, exist_ok=True)
        
        # 兼容不同版本的参数名
        max_retries = 3  # 增加重试次数
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 新版本使用 embedding_function
                if progress_callback:
                    progress_callback(88, f"🔄 正在创建向量数据库（尝试 {attempt + 1}/{max_retries}）...")
                vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding_function=embeddings,
                    persist_directory=db_path
                )
                break  # 成功创建，退出循环
            except TypeError as type_error:
                # 旧版本使用 embedding
                if progress_callback:
                    progress_callback(88, "🔄 正在创建向量数据库（使用兼容模式）...")
                try:
                    vectorstore = Chroma.from_documents(
                        documents=documents,
                        embedding=embeddings,
                        persist_directory=db_path
                    )
                    break  # 成功创建，退出循环
                except Exception as e:
                    last_error = e
                    # 检查是否是数据库错误（包括 HNSW 索引错误和 schema 错误）
                    error_msg = str(e).lower()
                    is_db_error = ("hnsw" in error_msg or "index" in error_msg or "compaction" in error_msg or 
                                  "segment" in error_msg or "no such column" in error_msg or 
                                  "collections.topic" in error_msg or "schema" in error_msg)
                    
                    if is_db_error and attempt < max_retries - 1:
                        # 如果是数据库错误，强制清理数据库并重试
                        if progress_callback:
                            progress_callback(87, "🔄 检测到数据库错误（可能是版本兼容性问题），强制清理并重试...")
                        import time
                        cleanup_corrupted_db(db_path, force=True)
                        time.sleep(1)  # 等待文件系统完全释放
                        if not os.path.exists(db_path):
                            os.makedirs(db_path, exist_ok=True)
                        continue
                    elif is_db_error:
                        # 重试次数用完，但仍然抛出详细错误
                        raise Exception(f"创建向量数据库失败（兼容模式，已重试 {max_retries} 次）: {str(e)}\n\n"
                                      f"检测到数据库错误（可能是版本兼容性问题），已尝试清理并重试，但仍然失败。\n"
                                      f"错误类型: {error_msg}\n\n"
                                      f"解决方案:\n"
                                      f"1. 手动删除数据库目录: {db_path}\n"
                                      f"2. 检查 ChromaDB 版本兼容性\n"
                                      f"3. 尝试降级 ChromaDB: poetry add chromadb==0.4.22") from e
                    else:
                        # 其他错误，直接抛出
                        raise Exception(f"创建向量数据库失败（兼容模式）: {str(e)}") from e
            except Exception as create_error:
                last_error = create_error
                error_msg = str(create_error).lower()
                # 检查是否是数据库错误（包括 HNSW 索引错误和 schema 错误）
                is_db_error = ("hnsw" in error_msg or "index" in error_msg or "compaction" in error_msg or 
                              "segment" in error_msg or "no such column" in error_msg or 
                              "collections.topic" in error_msg or "schema" in error_msg)
                
                if is_db_error and attempt < max_retries - 1:
                    # 如果是数据库错误，强制清理数据库并重试
                    if progress_callback:
                        progress_callback(87, "🔄 检测到数据库错误（可能是版本兼容性问题），强制清理并重试...")
                    import time
                    cleanup_corrupted_db(db_path, force=True)
                    time.sleep(1)  # 等待文件系统完全释放
                    if not os.path.exists(db_path):
                        os.makedirs(db_path, exist_ok=True)
                    continue
                elif is_db_error:
                    # 重试次数用完，但仍然抛出详细错误
                    error_type = type(create_error).__name__
                    raise Exception(f"创建向量数据库时出错 [{error_type}]（已重试 {max_retries} 次）: {str(create_error)}\n\n"
                                  f"检测到数据库错误（可能是版本兼容性问题），已尝试清理并重试，但仍然失败。\n"
                                  f"错误类型: {error_msg}\n\n"
                                  f"解决方案:\n"
                                  f"1. 手动删除数据库目录: {db_path}\n"
                                  f"2. 检查 ChromaDB 版本兼容性\n"
                                  f"3. 尝试降级 ChromaDB: poetry add chromadb==0.4.22") from create_error
                else:
                    # 其他错误，直接抛出
                    error_type = type(create_error).__name__
                    raise Exception(f"创建向量数据库时出错 [{error_type}]: {str(create_error)}") from create_error
        else:
            # 所有重试都失败了
            if last_error:
                error_type = type(last_error).__name__
                raise Exception(f"创建向量数据库失败（已重试 {max_retries} 次） [{error_type}]: {str(last_error)}") from last_error
            else:
                raise Exception("创建向量数据库失败：未知错误")
        
        if progress_callback:
            progress_callback(100, "✅ 向量数据库创建完成！")
        
        # 保存文档签名
        if folder_path:
            save_docs_signature(docs_dict, folder_path)
        
        return vectorstore
    except ImportError as e:
        # 导入错误，可能是缺少依赖包
        error_msg = str(e)
        if 'st' in globals():
            st.warning(f"⚠️ 向量数据库功能不可用（缺少依赖包）: {error_msg}\n\n💡 提示：\n- 向量搜索功能将不可用\n- 文档阅读和问答功能仍可正常使用\n- 如需使用向量搜索，请安装: pip install langchain-text-splitters langchain-community chromadb")
        return None
    except Exception as e:
        # 其他错误，显示详细错误信息
        error_msg = str(e)
        error_type = type(e).__name__
        
        # 检查是否是 NumPy 2.0 兼容性问题
        is_numpy_error = ("np.float_" in error_msg or "numpy" in error_msg.lower() or 
                         "AttributeError" in error_type and "float_" in error_msg)
        
        # 记录错误到控制台（用于调试）
        import traceback
        print(f"❌ 向量数据库创建失败:")
        print(f"   错误类型: {error_type}")
        print(f"   错误信息: {error_msg}")
        print(f"   详细堆栈:")
        traceback.print_exc()
        
        if 'st' in globals():
            if is_numpy_error:
                # NumPy 2.0 兼容性错误
                st.error(f"⚠️ **向量数据库创建失败 - NumPy 版本不兼容**\n\n"
                        f"**错误类型**: `{error_type}`\n\n"
                        f"**错误信息**: {error_msg}\n\n"
                        f"**问题原因**:\n"
                        f"ChromaDB 不兼容 NumPy 2.0，当前环境可能安装了 NumPy 2.0\n\n"
                        f"**解决方案**:\n"
                        f"1. **降级 NumPy 到 1.x 版本**（推荐）:\n"
                        f"   ```bash\n"
                        f"   poetry remove numpy\n"
                        f"   poetry add \"numpy>=1.24.0,<2.0.0\"\n"
                        f"   ```\n"
                        f"   或使用 pip:\n"
                        f"   ```bash\n"
                        f"   pip install \"numpy>=1.24.0,<2.0.0\"\n"
                        f"   ```\n\n"
                        f"2. **重新安装所有依赖**:\n"
                        f"   ```bash\n"
                        f"   poetry install\n"
                        f"   ```\n\n"
                        f"3. **检查 NumPy 版本**:\n"
                        f"   ```bash\n"
                        f"   poetry run python -c \"import numpy; print(numpy.__version__)\"\n"
                        f"   ```\n\n"
                        f"💡 **提示**: 修复后重新运行程序即可")
            else:
                # 其他错误
                st.error(f"⚠️ **向量数据库创建失败**\n\n"
                        f"**错误类型**: `{error_type}`\n\n"
                        f"**错误信息**: {error_msg}\n\n"
                        f"**可能的原因**:\n"
                        f"- 文档内容为空或格式不正确\n"
                        f"- 嵌入模型加载失败（检查网络连接或模型文件）\n"
                        f"- ChromaDB 版本不兼容\n"
                        f"- NumPy 版本不兼容（NumPy 2.0 不兼容）\n"
                        f"- 磁盘空间不足或没有写入权限\n"
                        f"- 内存不足（文档太大）\n\n"
                        f"**解决方案**:\n"
                        f"1. 检查文档是否为空\n"
                        f"2. 检查控制台输出的详细错误信息\n"
                        f"3. 尝试减少文档数量或大小\n"
                        f"4. 检查磁盘空间和权限\n"
                        f"5. 如果问题持续，请查看完整错误堆栈\n\n"
                        f"💡 **提示**: 向量搜索功能将不可用，但文档阅读和问答功能仍可正常使用（会使用所有文档内容，可能较慢）")
        return None

# DeepSeek API接口
def query_deepseek(prompt: str, api_key: str, model: str = "deepseek-chat", max_tokens: int = 2000, 
                   max_retries: int = 3, timeout: int = None):
    """调用DeepSeek API，带重试机制
    
    Args:
        prompt: 提示文本
        api_key: DeepSeek API密钥
        model: 模型名称
        max_tokens: 最大token数
        max_retries: 最大重试次数
        timeout: 超时时间（秒），如果为None则使用默认值或从session_state获取
    """
    import requests
    import time
    
    # 从 session_state 获取超时和重试配置（如果可用）
    if timeout is None:
        if 'st' in globals() and hasattr(st, 'session_state'):
            timeout = st.session_state.get('api_timeout', 60)
        else:
            timeout = 60
    
    if max_retries is None or max_retries == 3:
        if 'st' in globals() and hasattr(st, 'session_state'):
            max_retries = st.session_state.get('api_max_retries', 3)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个有帮助的助手，请基于提供的文档内容回答问题。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    
    # 重试机制
    for attempt in range(max_retries):
        try:
            # 根据尝试次数增加超时时间
            current_timeout = timeout + (attempt * 20)
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=current_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "API返回格式异常，请重试"
            elif response.status_code == 401:
                return "API密钥无效，请检查您的DeepSeek API密钥"
            elif response.status_code == 429:
                wait_time = 2 ** attempt  # 指数退避：2秒、4秒、8秒
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    continue
                return "API请求频率过高，请稍后再试"
            elif response.status_code == 500:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return "DeepSeek服务器错误，请稍后重试"
            else:
                return f"API请求失败 (状态码: {response.status_code}): {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                error_msg = f"请求超时（已尝试 {attempt + 1}/{max_retries} 次），{wait_time}秒后重试..."
                if 'st' in globals():
                    st.warning(error_msg)
                time.sleep(wait_time)
                continue
            else:
                return f"请求超时（已重试 {max_retries} 次）。可能的原因：\n1. 网络连接不稳定\n2. 请求内容过长\n3. DeepSeek服务器响应慢\n\n建议：\n- 检查网络连接\n- 尝试减少文档内容\n- 稍后重试"
        
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                error_msg = f"连接错误（已尝试 {attempt + 1}/{max_retries} 次），{wait_time}秒后重试..."
                if 'st' in globals():
                    st.warning(error_msg)
                time.sleep(wait_time)
                continue
            else:
                return "无法连接到DeepSeek API服务器。请检查：\n1. 网络连接是否正常\n2. 是否可以使用代理访问\n3. DeepSeek服务是否正常"
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return f"网络请求异常: {str(e)}"
        
        except Exception as e:
            return f"调用API时出错: {str(e)}"
    
    return "API调用失败，已重试多次仍无法成功"

def search_similar_documents(vectorstore, query: str, k: int = 4):
    """检索相似文档片段"""
    if vectorstore is None:
        return []
    
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return [(doc.page_content, doc.metadata["source"]) for doc in docs]
    except:
        return []

def answer_with_deepseek(question: str, vectorstore, docs_dict: Dict[str, Any], api_key: str):
    """使用DeepSeek回答问题"""
    # 检索相关文档片段
    similar_docs = search_similar_documents(vectorstore, question)
    
    if not similar_docs:
        # 如果没有向量数据库，使用所有文档内容
        context = "\n\n".join([f"文件: {name}\n内容: {data['content'][:2000]}..." 
                             for name, data in docs_dict.items()])
    else:
        # 使用检索到的文档片段
        context_parts = []
        for content, source in similar_docs:
            context_parts.append(f"来自文档 '{source}' 的内容:\n{content}")
        context = "\n\n".join(context_parts)
    
    # 构建提示
    prompt = f"""基于以下文档内容，请回答这个问题：{question}

相关文档内容：
{context[:8000]}  # 限制上下文长度

请基于上述文档内容回答，如果文档中没有相关信息，请明确说明。"""

    return query_deepseek(prompt, api_key)

def generate_summary_deepseek(docs_dict: Dict[str, Any], api_key: str, specific_files: List[str] = None):
    """使用DeepSeek生成总结报告"""
    # 提取内容
    contents = []
    if specific_files:
        for filename in specific_files:
            if filename in docs_dict:
                content = docs_dict[filename]['content']
                if isinstance(content, dict):
                    content = "\n".join([f"{k}: {v[:1000]}" for k, v in content.items()])
                contents.append(f"文件: {filename}\n{content}")
    else:
        for filename, data in docs_dict.items():
            content = data['content']
            if isinstance(content, dict):
                content = "\n".join([f"{k}: {v[:1000]}" for k, v in content.items()])
            contents.append(f"文件: {filename}\n{content}")
    
    combined_content = "\n\n".join(contents)
    
    # 构建提示
    prompt = f"""请根据以下文档内容，生成一份详细的总结报告：

文档内容：
{combined_content[:12000]}

请生成包括以下部分的报告：
1. 整体内容概述
2. 核心要点总结
3. 关键数据/信息提取
4. 主要发现和洞察
5. 建议和下一步行动

报告："""

    return query_deepseek(prompt, api_key, max_tokens=3000)

# 显示版权信息
def show_footer():
    """在页面底部显示版权信息"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px 0;'>
            <p style='margin: 5px 0;'><strong>Copyright © 2026 吕滢</strong></p>
            <p style='margin: 5px 0;'>
                GitHub: <a href='https://github.com/lveyond' target='_blank' style='color: #1f77b4;'>@lveyond</a> | 
                QQ/WeChat: 329613507
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Streamlit界面
def main():
    st.set_page_config(
        page_title="智能知识库系统 (DeepSeek版)",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 智能知识库系统 (DeepSeek版)")
    st.markdown("---")
    
    # 初始化session state
    if 'docs' not in st.session_state:
        st.session_state.docs = {}
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_key_loaded' not in st.session_state:
        st.session_state.api_key_loaded = False
    if 'is_creating_vectorstore' not in st.session_state:
        st.session_state.is_creating_vectorstore = False
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # DeepSeek API配置
        st.subheader("🔑 DeepSeek API设置")
        
        # 尝试从本地加载 API key
        saved_api_key = None
        if not st.session_state.api_key_loaded:
            saved_api_key = load_api_key()
            if saved_api_key:
                st.session_state.api_key_loaded = True
                st.session_state.saved_api_key = saved_api_key
                st.success("✅ 已从本地加载 API 密钥")
        
        # 使用保存的 key 或用户输入
        default_key = st.session_state.get('saved_api_key', '') if st.session_state.api_key_loaded else ''
        api_key_input = st.text_input(
            "DeepSeek API密钥", 
            value=default_key,
            type="password", 
            help="在 https://platform.deepseek.com/ 获取API密钥\n💾 密钥会自动保存到本地，下次启动无需重新输入"
        )
        
        # API key 管理按钮
        col_key1, col_key2 = st.columns(2)
        with col_key1:
            if st.button("💾 保存密钥", use_container_width=True):
                if api_key_input:
                    if save_api_key(api_key_input):
                        st.session_state.saved_api_key = api_key_input
                        st.session_state.api_key_loaded = True
                        st.success("✅ API 密钥已保存到本地")
                        st.rerun()
                else:
                    st.warning("请输入 API 密钥")
        
        with col_key2:
            if st.button("🗑️ 清除密钥", use_container_width=True):
                if delete_api_key():
                    st.session_state.saved_api_key = ""
                    st.session_state.api_key_loaded = False
                    st.success("✅ 已清除本地保存的 API 密钥")
                    st.rerun()
        
        # 自动保存逻辑：如果用户输入了新密钥且与保存的不同，自动保存
        if api_key_input and api_key_input != st.session_state.get('saved_api_key', ''):
            # 用户输入了新密钥，自动保存（仅在首次输入时，静默保存）
            if not st.session_state.api_key_loaded or api_key_input != saved_api_key:
                if save_api_key(api_key_input, show_error=False):
                    st.session_state.saved_api_key = api_key_input
                    st.session_state.api_key_loaded = True
                    # 静默保存，不显示提示（避免频繁刷新）
        
        # 使用输入的 key（优先使用新输入的）
        api_key = api_key_input if api_key_input else (st.session_state.get('saved_api_key', '') if st.session_state.api_key_loaded else '')
        
        # 显示保存状态
        if os.path.exists(CONFIG_FILE):
            saved_time = ""
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    saved_time = config.get("saved_at", "")
            except:
                pass
            if saved_time:
                st.caption(f"💾 密钥已保存（{saved_time}）")
            else:
                st.caption("💾 密钥已保存到本地")
        else:
            st.caption("💡 输入密钥后会自动保存到本地")
        
        # 模型选择
        model_choice = st.selectbox(
            "选择模型",
            ["deepseek-chat", "deepseek-coder"],
            help="deepseek-chat: 通用对话模型\ndeepseek-coder: 代码专用模型"
        )
        
        # API 超时和重试配置
        if 'api_timeout' not in st.session_state:
            st.session_state.api_timeout = 60
        if 'api_max_retries' not in st.session_state:
            st.session_state.api_max_retries = 3
        
        with st.expander("⚙️ 高级设置（网络问题时可调整）", expanded=False):
            timeout_seconds = st.slider(
                "请求超时时间（秒）",
                min_value=30,
                max_value=180,
                value=st.session_state.api_timeout,
                step=10,
                help="如果经常超时，可以增加此值"
            )
            max_retries = st.slider(
                "最大重试次数",
                min_value=1,
                max_value=5,
                value=st.session_state.api_max_retries,
                step=1,
                help="网络不稳定时可以增加重试次数"
            )
            
            # 保存到 session state
            st.session_state.api_timeout = timeout_seconds
            st.session_state.api_max_retries = max_retries
        
        st.markdown("---")
        st.header("📁 文件管理")
        
        # 文件夹选择
        folder_path = st.text_input("文件夹路径", placeholder="输入文件夹路径，如: ./documents")
        
        col1, col2 = st.columns(2)
        with col1:
            # 检查是否正在创建向量数据库
            is_creating_vectorstore = st.session_state.get('is_creating_vectorstore', False)
            
            if st.button("📂 加载文件夹", use_container_width=True, disabled=is_creating_vectorstore):
                if folder_path and os.path.exists(folder_path) and os.path.isdir(folder_path):
                    with st.spinner("正在读取文件..."):
                        st.session_state.docs = process_folder(folder_path)
                        # 保存当前文件夹路径
                        st.session_state.current_folder_path = folder_path
                    st.success(f"已加载 {len(st.session_state.docs)} 个文件")
                    
                    # 检查并加载/创建向量数据库
                    if st.session_state.docs:
                        st.session_state.is_creating_vectorstore = True
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # 首先尝试加载已有向量数据库
                            status_text.text("🔄 正在检查已有向量数据库...")
                            progress_bar.progress(5)
                            
                            existing_vectorstore = load_existing_vector_store(
                                folder_path=folder_path,
                                progress_callback=lambda p, msg: (
                                    progress_bar.progress(p / 100.0),
                                    status_text.text(msg)
                                )
                            )
                            
                            # 检查文档是否变化
                            docs_changed = check_docs_changed(st.session_state.docs, folder_path)
                            
                            # 安全地检查向量数据库是否可用（避免索引损坏导致的错误）
                            vectorstore_usable = False
                            if existing_vectorstore:
                                try:
                                    # 尝试访问向量数据库，如果索引损坏会在这里失败
                                    _ = len(existing_vectorstore)
                                    vectorstore_usable = True
                                except Exception as e:
                                    # 向量数据库索引可能损坏，需要重新创建
                                    vectorstore_usable = False
                                    status_text.text("⚠️ 检测到向量数据库索引损坏，将重新创建...")
                                    progress_bar.progress(0.1)
                            
                            if vectorstore_usable and not docs_changed:
                                # 文档未变化，使用已有向量数据库
                                st.session_state.vectorstore = existing_vectorstore
                                progress_bar.progress(100)
                                status_text.text("✅ 已加载已有向量数据库！")
                                st.success("✅ 已加载已有向量数据库（文档未变化）")
                            else:
                                # 文档变化或不存在，需要重新创建
                                if existing_vectorstore and docs_changed:
                                    status_text.text("📝 检测到文档变化，正在重新创建向量数据库...")
                                    progress_bar.progress(10)
                                
                                status_text.text("🔄 步骤 1/4: 准备文本内容...")
                                progress_bar.progress(10)
                                
                                status_text.text("🔄 步骤 2/4: 分割文本...")
                                progress_bar.progress(30)
                                
                                status_text.text("🔄 步骤 3/4: 生成向量嵌入（这可能需要几分钟）...")
                                progress_bar.progress(50)
                                
                                st.session_state.vectorstore = create_local_vector_store(
                                    st.session_state.docs,
                                    folder_path=folder_path,
                                    progress_callback=lambda p, msg: (
                                        progress_bar.progress(p / 100.0),
                                        status_text.text(msg)
                                    )
                                )
                                
                                progress_bar.progress(90)
                                status_text.text("🔄 步骤 4/4: 保存向量数据库...")
                                
                                if st.session_state.vectorstore:
                                    progress_bar.progress(100)
                                    status_text.text("✅ 向量数据库创建完成！")
                                    st.success("✅ 向量数据库创建完成！")
                                else:
                                    progress_bar.empty()
                                    status_text.empty()
                                    # 如果创建失败，已经在 create_local_vector_store 中显示了警告
                        finally:
                            st.session_state.is_creating_vectorstore = False
                            # 清理进度条
                            import time
                            time.sleep(0.5)
                            progress_bar.empty()
                            status_text.empty()
                else:
                    st.error("请输入有效的文件夹路径")
        
        with col2:
            if st.button("🔄 重新加载", use_container_width=True, disabled=is_creating_vectorstore):
                st.session_state.docs = {}
                st.session_state.vectorstore = None
                st.session_state.is_creating_vectorstore = False
                st.rerun()
        
        # 文件上传
        st.subheader("或上传文件")
        uploaded_files = st.file_uploader(
            "选择文件",
            type=['txt', 'docx', 'pdf', 'xlsx', 'xls'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files and st.button("上传文件"):
            temp_dir = tempfile.mkdtemp()
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 读取文件
                filename = uploaded_file.name
                file_ext = filename.split('.')[-1].lower()
                
                try:
                    if file_ext == 'txt':
                        content = read_text_file(file_path)
                    elif file_ext == 'docx':
                        content = read_docx_file(file_path)
                    elif file_ext == 'pdf':
                        content = read_pdf_file(file_path)
                    elif file_ext in ['xlsx', 'xls']:
                        content = read_excel_file(file_path)
                    else:
                        content = f"不支持的文件类型: {file_ext}"
                    
                    st.session_state.docs[filename] = {
                        'path': file_path,
                        'content': content,
                        'type': file_ext,
                        'size': uploaded_file.size
                    }
                except Exception as e:
                    st.error(f"读取文件 {filename} 失败: {str(e)}")
            
            st.success(f"已上传 {len(uploaded_files)} 个文件")
            
            # 检查并加载/创建向量数据库（上传文件时 folder_path 为 None）
            if st.session_state.docs:
                st.session_state.is_creating_vectorstore = True
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # 首先尝试加载已有向量数据库
                    status_text.text("🔄 正在检查已有向量数据库...")
                    progress_bar.progress(5)
                    
                    existing_vectorstore = load_existing_vector_store(
                        folder_path=None,  # 上传文件时没有文件夹路径
                        progress_callback=lambda p, msg: (
                            progress_bar.progress(p / 100.0),
                            status_text.text(msg)
                        )
                    )
                    
                    # 检查文档是否变化
                    docs_changed = check_docs_changed(st.session_state.docs, None)
                    
                    # 安全地检查向量数据库是否可用
                    vectorstore_usable = False
                    if existing_vectorstore:
                        try:
                            _ = len(existing_vectorstore)
                            vectorstore_usable = True
                        except Exception as e:
                            vectorstore_usable = False
                            status_text.text("⚠️ 检测到向量数据库索引损坏，将重新创建...")
                            progress_bar.progress(0.1)
                    
                    if vectorstore_usable and not docs_changed:
                        # 文档未变化，使用已有向量数据库
                        st.session_state.vectorstore = existing_vectorstore
                        progress_bar.progress(100)
                        status_text.text("✅ 已加载已有向量数据库！")
                        st.success("✅ 已加载已有向量数据库（文档未变化）")
                    else:
                        # 文档变化或不存在，需要重新创建
                        if existing_vectorstore and docs_changed:
                            status_text.text("📝 检测到文档变化，正在重新创建向量数据库...")
                            progress_bar.progress(10)
                        
                        status_text.text("🔄 步骤 1/4: 准备文本内容...")
                        progress_bar.progress(10)
                        
                        status_text.text("🔄 步骤 2/4: 分割文本...")
                        progress_bar.progress(30)
                        
                        status_text.text("🔄 步骤 3/4: 生成向量嵌入（这可能需要几分钟）...")
                        progress_bar.progress(50)
                        
                        st.session_state.vectorstore = create_local_vector_store(
                            st.session_state.docs,
                            folder_path=None,  # 上传文件时没有文件夹路径
                            progress_callback=lambda p, msg: (
                                progress_bar.progress(p / 100.0),
                                status_text.text(msg)
                            )
                        )
                        
                        progress_bar.progress(90)
                        status_text.text("🔄 步骤 4/4: 保存向量数据库...")
                    
                    if st.session_state.vectorstore:
                        progress_bar.progress(100)
                        status_text.text("✅ 向量数据库更新完成！")
                        st.success("✅ 向量数据库更新完成！")
                    else:
                        progress_bar.empty()
                        status_text.empty()
                finally:
                    st.session_state.is_creating_vectorstore = False
                    import time
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_text.empty()
        
        # 文件统计
        if st.session_state.docs:
            st.markdown("---")
            st.header("📊 统计信息")
            total_files = len(st.session_state.docs)
            file_types = {}
            for data in st.session_state.docs.values():
                file_type = data['type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
            
            st.write(f"**文件总数**: {total_files}")
            for ftype, count in file_types.items():
                st.write(f"**{ftype}文件**: {count}个")
        
        st.markdown("---")
        
        # 向量数据库管理
        if st.session_state.docs:
            with st.expander("🗑️ 向量数据库管理", expanded=False):
                col_vdb1, col_vdb2 = st.columns(2)
                
                with col_vdb1:
                    # 获取当前文件夹的向量数据库路径
                    current_folder_path = st.session_state.get('current_folder_path', None)
                    if current_folder_path:
                        current_db_path = get_vector_db_path(current_folder_path)
                        if st.button("🗑️ 删除当前向量数据库", use_container_width=True):
                            import shutil
                            if os.path.exists(current_db_path):
                                try:
                                    shutil.rmtree(current_db_path)
                                    st.session_state.vectorstore = None
                                    st.success("✅ 当前向量数据库已删除")
                                    st.info("💡 下次加载相同文件夹时会自动重新创建")
                                except Exception as e:
                                    st.error(f"删除失败: {str(e)}")
                            else:
                                st.info("当前向量数据库不存在")
                    else:
                        if st.button("🗑️ 删除所有向量数据库", use_container_width=True):
                            import shutil
                            if os.path.exists("./chroma_db"):
                                try:
                                    shutil.rmtree("./chroma_db")
                                    st.session_state.vectorstore = None
                                    st.success("✅ 所有向量数据库已删除")
                                    st.info("💡 下次加载文档时会自动重新创建")
                                except Exception as e:
                                    st.error(f"删除失败: {str(e)}")
                            else:
                                st.info("向量数据库不存在")
                
                with col_vdb2:
                    # 显示所有向量数据库信息
                    if os.path.exists("./chroma_db"):
                        try:
                            import shutil
                            total_size = 0
                            db_count = 0
                            for item in os.listdir("./chroma_db"):
                                item_path = os.path.join("./chroma_db", item)
                                if os.path.isdir(item_path):
                                    db_count += 1
                                    total_size += sum(f.stat().st_size for f in Path(item_path).rglob('*') if f.is_file())
                            
                            size_mb = total_size / (1024 * 1024)
                            if db_count > 0:
                                st.caption(f"💾 共 {db_count} 个向量数据库")
                                st.caption(f"💾 总大小: {size_mb:.2f} MB")
                            else:
                                st.caption("💾 向量数据库存在")
                        except:
                            st.caption("💾 向量数据库存在")
                    else:
                        st.caption("💾 未创建向量数据库")
                
                # 显示 HuggingFace 缓存信息
                hf_cache_path = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
                if os.path.exists(hf_cache_path):
                    try:
                        hf_size = sum(f.stat().st_size for f in Path(hf_cache_path).rglob('*') if f.is_file())
                        hf_size_gb = hf_size / (1024 * 1024 * 1024)
                        st.caption(f"🤖 HuggingFace 模型缓存: {hf_size_gb:.2f} GB")
                        st.caption(f"   位置: {hf_cache_path}")
                        st.caption("   💡 如需清理，可手动删除该目录")
                    except:
                        pass
        
        st.caption("💡 提示：使用本地向量数据库进行语义搜索，无需API密钥")
    
    # 主界面
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 文档浏览器")
        
        if st.session_state.docs:
            # 文件列表
            files = list(st.session_state.docs.keys())
            selected_file = st.selectbox(
                "选择文件浏览",
                files,
                index=0,
                key="file_selector"
            )
            
            if selected_file:
                file_info = st.session_state.docs[selected_file]
                
                # 文件信息卡片
                st.info(f"""
                **文件信息**
                - 类型: {file_info['type'].upper()}
                - 大小: {file_info['size']:,} 字节
                """)
                
                # 内容显示
                with st.expander("📋 查看内容", expanded=True):
                    content = file_info['content']
                    if isinstance(content, dict):  # Excel文件
                        tab_names = list(content.keys())
                        tabs = st.tabs(tab_names)
                        for i, (sheet_name, sheet_content) in enumerate(content.items()):
                            with tabs[i]:
                                st.text_area(
                                    f"{sheet_name} 工作表",
                                    sheet_content,
                                    height=300,
                                    key=f"excel_{selected_file}_{i}"
                                )
                    else:
                        st.text_area(
                            "文件内容",
                            content,
                            height=400,
                            key=f"content_{selected_file}"
                        )
        
        # 批量操作
        if st.session_state.docs:
            st.markdown("---")
            st.subheader("📈 批量总结")
            
            # 文档选择选项
            summary_mode = st.radio(
                "选择总结范围",
                ["📚 所有文档", "📄 选择特定文档"],
                horizontal=True,
                help="选择要总结的文档范围"
            )
            
            selected_files_for_summary = []
            if summary_mode == "📄 选择特定文档":
                # 多选文档
                file_options = list(st.session_state.docs.keys())
                selected_files_for_summary = st.multiselect(
                    "选择要总结的文档（可多选）",
                    options=file_options,
                    default=[],
                    help="选择要包含在总结报告中的文档"
                )
                
                if not selected_files_for_summary:
                    st.info("💡 请至少选择一个文档")
                    summary_button_disabled = True
                else:
                    summary_button_disabled = False
                    st.info(f"✅ 已选择 {len(selected_files_for_summary)} 个文档")
            else:
                summary_button_disabled = False
                st.info(f"📚 将总结所有 {len(st.session_state.docs)} 个文档")
            
            # 生成报告按钮
            generate_summary_clicked = st.button(
                "生成知识库总结报告", 
                use_container_width=True,
                disabled=summary_button_disabled if summary_mode == "📄 选择特定文档" else False
            )
            
            # 处理生成总结报告的逻辑
            if generate_summary_clicked:
                if not api_key:
                    st.error("请先输入DeepSeek API密钥")
                else:
                    # 确定要总结的文档
                    if summary_mode == "📚 所有文档":
                        files_to_summarize = None  # None 表示所有文档
                        summary_title = f"所有文档总结（共 {len(st.session_state.docs)} 个文档）"
                    else:
                        files_to_summarize = selected_files_for_summary
                        summary_title = f"选定文档总结（共 {len(selected_files_for_summary)} 个文档）"
                    
                    with st.spinner(f"正在生成总结报告（{summary_title}）..."):
                        summary = generate_summary_deepseek(
                            st.session_state.docs, 
                            api_key,
                            specific_files=files_to_summarize
                        )
                        # 保存到 session state
                        st.session_state.summary = summary
                        st.session_state.summary_title = summary_title
                        # 保存文档列表信息用于后续显示
                        if files_to_summarize:
                            st.session_state.summary_files = files_to_summarize
                            st.session_state.summary_doc_count = len(files_to_summarize)
                        else:
                            st.session_state.summary_files = None
                            st.session_state.summary_doc_count = len(st.session_state.docs)
            
            # 显示总结报告（移到按钮if块外，确保始终显示在col1）
            if 'summary' in st.session_state and st.session_state.summary:
                st.markdown("---")
                summary_title_display = st.session_state.get('summary_title', '总结报告')
                with st.expander(f"📊 查看总结报告 - {summary_title_display}", expanded=True):
                    # 显示总结的文档信息
                    summary_files = st.session_state.get('summary_files', None)
                    summary_doc_count = st.session_state.get('summary_doc_count', 0)
                    if summary_files:
                        st.markdown(f"**总结的文档：** {', '.join(summary_files)}")
                    else:
                        st.markdown(f"**总结的文档：** 所有文档（共 {summary_doc_count} 个）")
                    st.markdown("---")
                    st.write(st.session_state.summary)
                
                # 保存报告选项
                st.markdown("#### 💾 保存报告")
                col_save1, col_save2, col_save3 = st.columns(3)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # 确定文档列表用于保存
                summary_files = st.session_state.get('summary_files', None)
                summary_doc_count = st.session_state.get('summary_doc_count', 0)
                if summary_files:
                    doc_list = summary_files
                    doc_count = len(summary_files)
                else:
                    doc_list = list(st.session_state.docs.keys())
                    doc_count = summary_doc_count
                
                # 生成 Markdown 格式内容
                md_summary = f"# {summary_title_display}\n\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n文档数量: {doc_count}\n\n---\n\n{st.session_state.summary}"
                
                with col_save1:
                    st.download_button(
                        label="📄 保存为TXT",
                        data=st.session_state.summary,
                        file_name=f"知识库总结_{timestamp}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col_save2:
                    st.download_button(
                        label="📝 保存为Markdown",
                        data=md_summary,
                        file_name=f"知识库总结_{timestamp}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col_save3:
                    # JSON格式（包含元数据）
                    json_data = {
                        "总结标题": summary_title_display,
                        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "文档数量": doc_count,
                        "文档列表": doc_list,
                        "总结内容": st.session_state.summary
                    }
                    st.download_button(
                        label="📊 保存为JSON",
                        data=json.dumps(json_data, ensure_ascii=False, indent=2),
                        file_name=f"知识库总结_{timestamp}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                # 自动保存到本地（可选）
                save_dir = os.path.join(".", "saved_reports")
                os.makedirs(save_dir, exist_ok=True)
                
                if st.checkbox("💾 同时自动保存到本地", value=False, key="auto_save_summary"):
                    try:
                        # 保存TXT版本
                        txt_path = os.path.join(save_dir, f"知识库总结_{timestamp}.txt")
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(st.session_state.summary)
                        
                        # 保存Markdown版本
                        md_path = os.path.join(save_dir, f"知识库总结_{timestamp}.md")
                        with open(md_path, 'w', encoding='utf-8') as f:
                            f.write(md_summary)
                        
                        st.success(f"✅ 报告已保存到: {save_dir}")
                        st.info(f"📁 文件路径:\n- {txt_path}\n- {md_path}")
                    except Exception as e:
                        st.error(f"保存失败: {str(e)}")
    
    with col2:
        st.header("🤖 智能问答")
        
        # 聊天历史
        if st.session_state.chat_history:
            with st.expander("🗣️ 对话历史", expanded=False):
                # 保存对话历史按钮
                col_history1, col_history2 = st.columns([3, 1])
                with col_history2:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # 生成对话历史文本
                    history_text = f"# 对话历史记录\n\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n文档数量: {len(st.session_state.docs)}\n\n---\n\n"
                    for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                        history_text += f"## 对话 {i}\n\n**问题:** {q}\n\n**回答:**\n{a}\n\n---\n\n"
                    
                    st.download_button(
                        label="💾 保存对话",
                        data=history_text,
                        file_name=f"对话历史_{timestamp}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                # 显示最近5条对话
                for i, (q, a) in enumerate(st.session_state.chat_history[-5:], start=len(st.session_state.chat_history)-4):  # 显示最近5条
                    st.markdown(f"**Q{i}:** {q}")
                    st.markdown(f"**A{i}:** {a}")
                    st.markdown("---")
        
        # 问题输入
        question = st.text_area(
            "输入您的问题",
            placeholder="例如：总结一下文档的主要内容是什么？或者：从这些文档中找出关于XX的信息。",
            height=100,
            key="question_input"
        )
        
        col_a, col_b, col_c = st.columns([1, 1, 2])
        
        with col_a:
            search_clicked = st.button("🔍 搜索答案", type="primary", use_container_width=True)
        
        with col_b:
            if st.button("🧹 清空对话", use_container_width=True):
                # 清空前询问是否保存
                if st.session_state.chat_history:
                    st.warning("⚠️ 清空对话前建议先保存对话历史！")
                st.session_state.chat_history = []
                st.rerun()
        
        with col_c:
            if st.button("💡 示例问题", use_container_width=True):
                examples = [
                    "总结所有文档的核心要点",
                    "提取文档中的关键数据",
                    "列出所有提到的重要日期",
                    "各文档之间的关联是什么？"
                ]
                st.session_state.question_input = st.session_state.get("question_input", "") + examples[0]
        
        # 处理搜索答案的逻辑（移到列布局外，使内容占据全宽）
        if search_clicked:
            # 清除高级功能显示状态
            st.session_state.show_data_analysis = False
            
            if not question:
                st.warning("请输入问题")
            elif not api_key:
                st.error("请输入DeepSeek API密钥")
            elif not st.session_state.docs:
                st.error("请先加载文档")
            else:
                # 显示超时提示（全宽）
                timeout_info = st.session_state.get('api_timeout', 60)
                retry_info = st.session_state.get('api_max_retries', 3)
                st.info(f"⏱️ 超时设置: {timeout_info}秒 | 重试次数: {retry_info}次 | 如遇超时可在侧边栏调整")
                
                with st.spinner(f"正在思考...（超时时间: {timeout_info}秒）"):
                    answer = answer_with_deepseek(
                        question, 
                        st.session_state.vectorstore, 
                        st.session_state.docs, 
                        api_key
                    )
                    
                    # 保存到历史
                    st.session_state.chat_history.append((question, answer))
                    
                    # 显示答案（全宽）
                    st.markdown("### 💡 答案")
                    st.write(answer)
                    
                    # 保存单个问答
                    col_save_qa1, col_save_qa2 = st.columns(2)
                    timestamp_qa = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # 生成问答内容
                    qa_text = f"# 问答记录\n\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## 问题\n\n{question}\n\n## 回答\n\n{answer}\n"
                    
                    with col_save_qa1:
                        st.download_button(
                            label="💾 保存此问答",
                            data=qa_text,
                            file_name=f"问答_{timestamp_qa}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col_save_qa2:
                        # 自动保存选项
                        if st.checkbox("自动保存", key=f"auto_save_{timestamp_qa}", value=False):
                            save_dir_qa = os.path.join(".", "saved_qa")
                            os.makedirs(save_dir_qa, exist_ok=True)
                            try:
                                qa_path = os.path.join(save_dir_qa, f"问答_{timestamp_qa}.md")
                                with open(qa_path, 'w', encoding='utf-8') as f:
                                    f.write(qa_text)
                                st.success(f"✅ 已保存到: {save_dir_qa}")
                            except Exception as e:
                                st.error(f"保存失败: {str(e)}")
                    
                    # 如果答案包含错误信息，提供解决建议
                    if "超时" in answer or "连接" in answer or "网络" in answer:
                        with st.expander("💡 网络问题解决建议", expanded=True):
                            st.markdown("""
                            **如果遇到超时或连接问题，可以尝试：**
                            1. 📈 **增加超时时间**：在侧边栏"高级设置"中增加超时时间（建议120-180秒）
                            2. 🔄 **增加重试次数**：在侧边栏"高级设置"中增加重试次数（建议4-5次）
                            3. 🌐 **检查网络**：确保网络连接稳定，可以访问 api.deepseek.com
                            4. 📝 **减少文档内容**：如果文档很大，尝试减少加载的文档数量
                            5. ⏰ **稍后重试**：可能是DeepSeek服务器繁忙，稍后再试
                            """)
                    
                    # 显示检索来源
                    if st.session_state.vectorstore:
                        with st.expander("查看参考来源"):
                            similar_docs = search_similar_documents(
                                st.session_state.vectorstore, 
                                question
                            )
                            for i, (content, source) in enumerate(similar_docs[:3], 1):
                                st.markdown(f"**来源 {i} - {source}**")
                                st.caption(content[:300] + "...")
        
        # 高级功能（在col2内，确保布局正确）
        st.markdown("---")
        st.subheader("🎯 高级功能")
        
        # 数据分析按钮（语义搜索功能已移除，因为与"查看参考来源"功能重复）
        data_analysis_clicked = st.button("📊 数据分析", use_container_width=True, key="data_analysis_btn")
        
        # 初始化session_state
        if 'show_data_analysis' not in st.session_state:
            st.session_state.show_data_analysis = False
        
        if data_analysis_clicked:
            st.session_state.show_data_analysis = True
        
        # 处理数据分析（在col2内，使用容器组织结果）
        if st.session_state.show_data_analysis:
            if not st.session_state.docs:
                st.warning("请先加载文档")
            elif not api_key:
                st.error("请输入DeepSeek API密钥")
            else:
                with st.spinner("正在分析文档..."):
                    prompt = f"""请分析以下文档集合，提供数据分析:

文档信息：
{chr(10).join([f'{name}: {len(str(data["content"]))} 字符' for name, data in st.session_state.docs.items()])}

请提供：
1. 文档内容分布分析
2. 潜在的数据模式和趋势
3. 建议的数据可视化方式"""
                    
                    analysis = query_deepseek(prompt, api_key)
                    st.markdown("### 📊 数据分析结果")
                    st.write(analysis)
        
        # 显示版权信息
        show_footer()

# 简易版（无向量数据库）
def simple_main():
    """简易版本，不使用向量数据库"""
    st.set_page_config(
        page_title="简易知识库浏览器",
        page_icon="📁",
        layout="wide"
    )
    
    st.title("📁 简易知识库浏览器")
    
    # 文件上传
    uploaded_files = st.file_uploader(
        "上传文件 (支持txt, docx, pdf, excel)",
        type=['txt', 'docx', 'pdf', 'xlsx', 'xls'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        docs = {}
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            # 保存上传的文件到临时目录
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 读取文件
            filename = uploaded_file.name
            file_ext = filename.split('.')[-1].lower()
            
            try:
                if file_ext == 'txt':
                    content = read_text_file(file_path)
                elif file_ext == 'docx':
                    content = read_docx_file(file_path)
                elif file_ext == 'pdf':
                    content = read_pdf_file(file_path)
                elif file_ext in ['xlsx', 'xls']:
                    content = read_excel_file(file_path)
                else:
                    content = f"不支持的文件类型"
                
                docs[filename] = {
                    'content': content,
                    'type': file_ext,
                    'path': file_path
                }
            except Exception as e:
                st.error(f"读取文件 {filename} 失败: {str(e)}")
        
        # 文件浏览器
        if docs:
            selected_file = st.selectbox("选择文件", list(docs.keys()))
            
            if selected_file in docs:
                content = docs[selected_file]['content']
                st.text_area("文件内容", 
                           str(content) if not isinstance(content, dict) else str(content),
                           height=400)
        
        # 简单问答
        st.markdown("---")
        
        # 尝试加载保存的 API key
        saved_api_key = load_api_key()
        default_key = saved_api_key if saved_api_key else ""
        
        col_simple_key1, col_simple_key2 = st.columns([3, 1])
        with col_simple_key1:
            api_key = st.text_input("DeepSeek API密钥", value=default_key, type="password")
        with col_simple_key2:
            if st.button("💾 保存", use_container_width=True):
                if api_key:
                    if save_api_key(api_key):
                        st.success("✅ 已保存")
                else:
                    st.warning("请输入密钥")
        
        question = st.text_input("输入问题")
        
        if st.button("获取答案") and api_key and question:
            # 合并所有文档内容
            all_content = ""
            for filename, data in docs.items():
                content = data['content']
                if isinstance(content, dict):
                    content = "\n".join([f"{k}: {v}" for k, v in content.items()])
                all_content += f"\n\n文件: {filename}\n{content}"
            
            # 调用DeepSeek
            prompt = f"""基于以下文档内容回答问题：

{all_content[:8000]}

问题：{question}

请基于文档内容回答，如果文档中没有相关信息，请明确说明。"""
            
            with st.spinner("正在思考..."):
                answer = query_deepseek(prompt, api_key)
                st.write("**答案：**", answer)
        
        # 显示版权信息
        show_footer()

if __name__ == "__main__":
    # 默认使用完整版，可以通过环境变量或命令行参数切换
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        simple_main()
    else:
        main()