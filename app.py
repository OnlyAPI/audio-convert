from log_config import setup_logger
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # 导入 CORS
import zipfile
import io
import os

from convert import handle_convert
from func import save_file_to_local, get_env_max_file_count, get_env_max_file_size, is_support_target_audio_ext, get_env_support_target_audio_ext, get_env_support_receive_audio_ext

app = Flask(__name__)
CORS(app=app)


# 使用 setup_logger 配置模块A的日志记录器
logger = setup_logger(__name__)


# 允许的最大文件数量
MAX_FILE_COUNT = get_env_max_file_count()
# 单个文件大小限制（单位：字节）
MAX_FILE_SIZE = get_env_max_file_size()


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Expose-Headers', 'Content-Disposition')
    return response



@app.route('/py-api/convert/audio', methods=['POST'])
def file_convert_mp3():
    '''
        上传需要转换格式的文件列表
        return: 转换后的压缩包文件
    '''
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    # 获取上传的文件
    files = request.files.getlist('files')
    
    # 检查文件数量
    if len(files) < 1 or len(files) > MAX_FILE_COUNT:
        return jsonify({"error": f"Number of files must be between 1 and {MAX_FILE_COUNT}"}), 400

    # 检查文件大小
    for file in files:
        if file.filename == '':
            return jsonify({"error": "One or more files have no filename"}), 400
        
        # 获取文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # 将指针重新设置到文件开始处
        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": f"File {file.filename} exceeds the maximum size of 50MB"}), 400

    # 获取请求字符串参数
    target_type = request.form.get('targetType')
    if not target_type:
        logger.error("目标转换类型不能为空")
        return jsonify({"error": "target type not be null."}), 400

    if not is_support_target_audio_ext(target_type):
        logger.error(f"不支持的目标音频格式: {target_type}")
        return jsonify({"error": f"Unsupported audio target type, Only supported: {get_env_support_target_audio_ext()}"}), 400


    # 保存文件到本地
    local_paths = save_file_to_local(files=files)
    mp3_result_paths = handle_convert(origin_audio_local_paths=local_paths, target_suffix=target_type)

    if not mp3_result_paths:
        return jsonify({'error': '转换失败'}), 400

    # 返回压缩包流
    zip_buffer = create_zip_from_file_path(mp3_result_paths)

    # 准备响应
    response = make_response(zip_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=converted.zip'
    response.headers['Content-Type'] = 'application/zip'
    
    return response


@app.route('/py-api/support/target-audio', methods=['GET'])
def get_support_target_ext():
    """
        获取支持的目标音频格式
    """
    return jsonify({'code': 0, 'msg': 'ok', 'data': sorted(list(get_env_support_target_audio_ext()))}), 200


@app.route('/py-api/support/receive-audio', methods=['GET'])
def get_support_receive_ext():
    """
        获取支持的输入音频格式
    """
    return jsonify({'code': 0, 'msg': 'ok', 'data': sorted(list(get_env_support_receive_audio_ext()))}), 200


'''
通过文件地址数组创建压缩包
'''
def create_zip_from_file_path(file_paths):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                zip_file.writestr(os.path.basename(file_path), file_data)
    zip_buffer.seek(0)
    return zip_buffer



