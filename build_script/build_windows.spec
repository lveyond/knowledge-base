# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec文件 - 用于打包Windows应用程序

import os
from pathlib import Path

block_cipher = None

# 获取项目根目录
# 脚本从项目根目录运行，所以当前工作目录就是项目根目录
import os

# 优先使用当前工作目录（脚本从项目根目录运行）
project_root = Path(os.getcwd())

# 验证路径是否正确（检查是否存在knowledge_base_deepseek.py）
if not (project_root / 'knowledge_base_deepseek.py').exists():
    # 如果找不到，尝试使用SPECPATH计算
    try:
        if 'SPECPATH' in globals():
            # spec文件在build_script目录中，所以parent.parent是项目根目录
            project_root = Path(SPECPATH).parent.parent
    except:
        pass

# 如果还是找不到，尝试使用相对路径
if not (project_root / 'knowledge_base_deepseek.py').exists():
    # 尝试从build_script的父目录查找
    project_root = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()

# 收集所有需要的数据文件
datas = []
# 如果存在prompt_templates目录，也包含进去
if (project_root / 'prompt_templates').exists():
    datas.append((str(project_root / 'prompt_templates'), 'prompt_templates'))

# 收集隐藏导入（PyInstaller可能无法自动检测的模块）
hiddenimports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.runtime.caching',
    'streamlit.runtime.metrics_util',
    'streamlit.runtime.legacy_caching',
    'streamlit.components.v1.components',
    'streamlit.elements',
    'streamlit.logger',
    'streamlit.proto',
    'streamlit.runtime',
    'streamlit.runtime.caching',
    'streamlit.runtime.caching.cache_utils',
    'streamlit.runtime.caching.cache_data_api',
    'streamlit.runtime.caching.cache_resource_api',
    'streamlit.runtime.legacy_caching',
    'streamlit.runtime.legacy_caching.hashing',
    'streamlit.runtime.state',
    'streamlit.runtime.state.session_state',
    'streamlit.runtime.uploaded_file_manager',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.file_util',
    'streamlit.config',
    'streamlit.config_option',
    'streamlit.config_util',
    'streamlit.source_util',
    'streamlit.string_util',
    'streamlit.util',
    'streamlit.watcher',
    'streamlit.watcher.path_watcher',
    'streamlit.watcher.event_based_path_watcher',
    'streamlit.watcher.polling_path_watcher',
    'streamlit.components',
    'streamlit.components.v1',
    'streamlit.components.v1.components',
    'streamlit.elements',
    'streamlit.elements.altair_chart',
    'streamlit.elements.arrow',
    'streamlit.elements.arrow_altair',
    'streamlit.elements.arrow_dataframe',
    'streamlit.elements.arrow_table',
    'streamlit.elements.audio',
    'streamlit.elements.bokeh_chart',
    'streamlit.elements.button',
    'streamlit.elements.camera_input',
    'streamlit.elements.checkbox',
    'streamlit.elements.color_picker',
    'streamlit.elements.dataframe',
    'streamlit.elements.data_editor',
    'streamlit.elements.date_input',
    'streamlit.elements.deck_gl_json_chart',
    'streamlit.elements.download_button',
    'streamlit.elements.empty',
    'streamlit.elements.exception',
    'streamlit.elements.file_uploader',
    'streamlit.elements.form',
    'streamlit.elements.graphviz_chart',
    'streamlit.elements.header',
    'streamlit.elements.iframe',
    'streamlit.elements.image',
    'streamlit.elements.json',
    'streamlit.elements.line_chart',
    'streamlit.elements.map',
    'streamlit.elements.markdown',
    'streamlit.elements.metric',
    'streamlit.elements.multiselect',
    'streamlit.elements.number_input',
    'streamlit.elements.plotly_chart',
    'streamlit.elements.progress',
    'streamlit.elements.pyplot',
    'streamlit.elements.radio',
    'streamlit.elements.selectbox',
    'streamlit.elements.select_slider',
    'streamlit.elements.slider',
    'streamlit.elements.snow',
    'streamlit.elements.text',
    'streamlit.elements.text_area',
    'streamlit.elements.text_input',
    'streamlit.elements.time_input',
    'streamlit.elements.toast',
    'streamlit.elements.vega_lite_chart',
    'streamlit.elements.video',
    'streamlit.elements.write',
    'streamlit.elements.widgets',
    'streamlit.elements.widgets.base_widget',
    'streamlit.elements.widgets.button',
    'streamlit.elements.widgets.checkbox',
    'streamlit.elements.widgets.color_picker',
    'streamlit.elements.widgets.data_editor',
    'streamlit.elements.widgets.date_input',
    'streamlit.elements.widgets.file_uploader',
    'streamlit.elements.widgets.multiselect',
    'streamlit.elements.widgets.number_input',
    'streamlit.elements.widgets.radio',
    'streamlit.elements.widgets.selectbox',
    'streamlit.elements.widgets.select_slider',
    'streamlit.elements.widgets.slider',
    'streamlit.elements.widgets.text_area',
    'streamlit.elements.widgets.text_input',
    'streamlit.elements.widgets.time_input',
    'streamlit.elements.widgets.widget',
    'streamlit.logger',
    'streamlit.proto',
    'streamlit.proto.Alert_pb2',
    'streamlit.proto.Arrow_pb2',
    'streamlit.proto.ArrowNamedDataSet_pb2',
    'streamlit.proto.Block_pb2',
    'streamlit.proto.Button_pb2',
    'streamlit.proto.ChatInput_pb2',
    'streamlit.proto.Checkbox_pb2',
    'streamlit.proto.Code_pb2',
    'streamlit.proto.ColorPicker_pb2',
    'streamlit.proto.ComponentInstance_pb2',
    'streamlit.proto.ConfusionMatrix_pb2',
    'streamlit.proto.Dataframe_pb2',
    'streamlit.proto.DateInput_pb2',
    'streamlit.proto.Delta_pb2',
    'streamlit.proto.DocString_pb2',
    'streamlit.proto.DownloadButton_pb2',
    'streamlit.proto.Element_pb2',
    'streamlit.proto.Exception_pb2',
    'streamlit.proto.FileUploader_pb2',
    'streamlit.proto.ForwardMsg_pb2',
    'streamlit.proto.Frame_pb2',
    'streamlit.proto.GraphVizChart_pb2',
    'streamlit.proto.IFrame_pb2',
    'streamlit.proto.Image_pb2',
    'streamlit.proto.Index_pb2',
    'streamlit.proto.LabelVisibilityMessage_pb2',
    'streamlit.proto.Markdown_pb2',
    'streamlit.proto.Metric_pb2',
    'streamlit.proto.MultiSelect_pb2',
    'streamlit.proto.NamedDataSet_pb2',
    'streamlit.proto.NumberInput_pb2',
    'streamlit.proto.PageConfig_pb2',
    'streamlit.proto.PageInfo_pb2',
    'streamlit.proto.PageNotFound_pb2',
    'streamlit.proto.PlotlyChart_pb2',
    'streamlit.proto.Progress_pb2',
    'streamlit.proto.Radio_pb2',
    'streamlit.proto.Selectbox_pb2',
    'streamlit.proto.SelectSlider_pb2',
    'streamlit.proto.SessionEvent_pb2',
    'streamlit.proto.SessionState_pb2',
    'streamlit.proto.SessionStatus_pb2',
    'streamlit.proto.Slider_pb2',
    'streamlit.proto.Snow_pb2',
    'streamlit.proto.Spinner_pb2',
    'streamlit.proto.TextArea_pb2',
    'streamlit.proto.TextInput_pb2',
    'streamlit.proto.TimeInput_pb2',
    'streamlit.proto.Toast_pb2',
    'streamlit.proto.VegaLiteChart_pb2',
    'streamlit.proto.Video_pb2',
    'streamlit.proto.WidgetStates_pb2',
    'streamlit.runtime',
    'streamlit.runtime.caching',
    'streamlit.runtime.caching.cache_utils',
    'streamlit.runtime.caching.cache_data_api',
    'streamlit.runtime.caching.cache_resource_api',
    'streamlit.runtime.legacy_caching',
    'streamlit.runtime.legacy_caching.hashing',
    'streamlit.runtime.state',
    'streamlit.runtime.state.session_state',
    'streamlit.runtime.uploaded_file_manager',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.file_util',
    'streamlit.config',
    'streamlit.config_option',
    'streamlit.config_util',
    'streamlit.source_util',
    'streamlit.string_util',
    'streamlit.util',
    'streamlit.watcher',
    'streamlit.watcher.path_watcher',
    'streamlit.watcher.event_based_path_watcher',
    'streamlit.watcher.polling_path_watcher',
    'streamlit.components',
    'streamlit.components.v1',
    'streamlit.components.v1.components',
    # LangChain相关
    'langchain',
    'langchain_community',
    'langchain_core',
    'langchain_text_splitters',
    'langchain_huggingface',
    'langchain_chroma',
    # ChromaDB相关
    'chromadb',
    'chromadb.db',
    'chromadb.api',
    'chromadb.api.models',
    'chromadb.api.types',
    'chromadb.config',
    'chromadb.telemetry',
    'chromadb.telemetry.events',
    'chromadb.telemetry.posthog',
    'chromadb.telemetry.product',
    'chromadb.utils',
    'chromadb.utils.embedding_functions',
    # 文档处理相关
    'docx',
    'pypdf',
    'openpyxl',
    # AI模型相关
    'sentence_transformers',
    'transformers',
    'torch',
    'requests',
    # 其他
    'pandas',
    'numpy',
    'altair',
    'plotly',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'pkg_resources.py2_warn',
]

# 确保launcher.py路径正确
launcher_path = project_root / 'build_script' / 'launcher.py'
# 如果找不到，尝试使用相对路径（从当前工作目录）
if not launcher_path.exists():
    launcher_path = Path('build_script') / 'launcher.py'
    if not launcher_path.exists():
        # 最后尝试从spec文件所在目录
        try:
            if 'SPECPATH' in globals():
                launcher_path = Path(SPECPATH).parent / 'launcher.py'
        except:
            pass

# 确保主程序文件路径正确
main_file_path = project_root / 'knowledge_base_deepseek.py'
# 如果找不到，尝试使用相对路径
if not main_file_path.exists():
    main_file_path = Path('knowledge_base_deepseek.py')

a = Analysis(
    [str(launcher_path)],  # 使用启动器作为入口点
    pathex=[str(project_root)],
    binaries=[],
    datas=datas + [
        (str(main_file_path), '.'),  # 包含主程序文件
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='智能知识库系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 显示控制台窗口，方便调试
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='智能知识库系统',
)
