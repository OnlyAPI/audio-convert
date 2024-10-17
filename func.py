from datetime import datetime
import os
from pathlib import Path
import platform

from application import env
from log_config import setup_logger

# 使用 setup_logger 配置模块A的日志记录器
logger = setup_logger(__name__)



#************************************************application.py 方法**************************************************************
def get_env_path_upload():
    return env.get('path').get('upload')

def get_env_path_converted():
    return env.get('path').get('converted')

def get_env_ffmpeg_path():
    return env.get('ffmpeg_path')

def get_env_max_file_count():
    return env.get('max_file_count')

def get_env_max_file_size():
    return env.get('max_file_size')

def get_env_support_receive_audio_ext():
    return env.get('support_receive_audio_ext')

def get_env_support_target_audio_ext():
    return env.get('support_target_audio_ext')


#*************************************************************其他方法**********************************************************************

def getTodayStr():
    """
        获取今天的日期
    """
    today = datetime.now()
    # 将昨天的日期格式化为 "yyyy-MM-dd" 格式的字符串
    return today.strftime("%Y/%m/%d")


    
def get_current_timestamp():
    """
        获取当前时间戳（以秒为单位），然后转换成毫秒
    """
    now = datetime.now()
    timestamp = int(now.timestamp() * 1000)
    return timestamp


def get_full_path(prefix_path) -> str:
    """
        获取加上今天日期的完整路径
    """
    today = getTodayStr()
    # 使用 os.path.join() 来确保路径分隔符正确
    local_path = os.path.join(prefix_path, *today.split('/'))

    if not os.path.exists(local_path):
        # 如果文件夹不存在，则创建它
        os.makedirs(local_path)
    return local_path


def get_file_name_by_path(path):
    """
        通过路径获取文件名
    """
    # 创建一个 Path 对象
    path = Path(path)

    # 获取文件名
    return path.name


def get_current_system_name():
    # 获取操作系统名称
    return platform.system()


def get_upload_path_by_file_name(fileName):
    """
        获取上传音频文件路径
    """
    return f"{get_full_path(get_env_path_upload())}/{fileName}"


def get_converted_path_by_file_name(fileName):
    """
        获取转换后文件路径
    """
    return f"{get_full_path(get_env_path_converted())}/{fileName}"



def get_current_system_ffmpeg_path():
    return get_env_ffmpeg_path().get(get_current_system_name()).get('ffmpeg')


def get_current_system_ffprobe_path():
    return get_env_ffmpeg_path().get(get_current_system_name()).get('ffprobe')



def get_file_suffix(fileName):
    """
        获取文件扩展名，不带·
    """
    # 使用os.path.splitext 提取扩展名
    _, extension = os.path.splitext(fileName)

    # 扩展名通常包括点号，如果不需要点号，可以这样处理
    extension_without_dot = extension[1:] if extension.startswith('.') else extension

    return extension_without_dot


def save_file_to_local(files):
    '''
        保存文件到本地
    '''
    local_path = []
    try:
        for file in files:
            filename = file.filename  # 获取文件名
            file_path = get_upload_path_by_file_name(fileName=filename)
            file.save(file_path)
            local_path.append(file_path)
            logger.info(f'{file.filename} 保存本地成功')
    except Exception:
        logger.error(f'{file.filename} 保存本地失败')
    return local_path


def is_support_receive_audio_ext(audio_ext):
    """ 判断文件是否是支持的输入音频扩展 """
    return audio_ext in get_env_support_receive_audio_ext()

def is_support_target_audio_ext(target_ext):
    """ 判断文件是否是支持的目标音频扩展 """
    return target_ext in get_env_support_target_audio_ext()



if __name__ == '__main__':
    # print(get_current_system_ffmpeg_path())
    # print(is_support_receive_audio_ext(audio_ext='aaa.mp4'))
    name, extension = os.path.splitext("s.png/#ffaaamp4")
    print(name)
    print(extension)
