import os
from pydub import AudioSegment
import shutil

from func import get_file_name_by_path, get_converted_path_by_file_name, get_current_timestamp, get_current_system_ffmpeg_path, get_current_system_ffprobe_path,get_file_suffix, is_support_receive_audio_ext
from log_config import setup_logger


# 使用 setup_logger 配置模块A的日志记录器
logger = setup_logger(__name__)

# 设置 pydub 使用的路径
AudioSegment.converter = get_current_system_ffmpeg_path()
AudioSegment.ffmpeg = get_current_system_ffmpeg_path()
AudioSegment.ffprobe = get_current_system_ffprobe_path()


def audio_file_2_mp3(origin_audio_local_paths: list) -> list:
    """
        音频文件转MP3
    """
    return handle_convert(origin_audio_local_paths, 'mp3')



def handle_convert(origin_audio_local_paths, target_suffix):
    """
        通用文件转目标格式

        params:
            origin_audio_local_paths: 需要转换格式的源文件路径
            target_suffix: 目标格式，不带·
    """
    result_paths = []
    for audio_path in origin_audio_local_paths:

        audio_file_name = get_file_name_by_path(path=audio_path)

        if audio_file_name.endswith(target_suffix):
            logger.info(f"{audio_path}此文件为mp3文件, 输出源路径.")
            result_paths.append(audio_path)
            continue
        
        # 音频文件扩展名，不带.
        audio_ext = get_file_suffix(audio_file_name)

        if not is_support_receive_audio_ext(audio_ext):
            logger.info(f'不支持的原音频格式: {audio_path}')
            continue
        
        target_path = get_converted_path_by_file_name(os.path.splitext(audio_file_name)[0] + f".{target_suffix}")
        # 打印文件路径以进行调试
        logger.info(f"转换{audio_path} >>>>>> {target_path}")
        start_time = get_current_timestamp()
        
        # 加载音频文件
        audio = AudioSegment.from_file(audio_path, format=f"{audio_ext}")
        
        # 导出为 .mp3 格式
        audio.export(target_path, format=f"{target_suffix}")

        end_time = get_current_timestamp()
        logger.info(f"{audio_file_name}转{target_suffix}完成, 耗时: {end_time - start_time}毫秒")

        result_paths.append(target_path)

    return result_paths


def local_handle(input_directory, target_directory):
    """
        直接调用方法处理文件
    """
    # 遍历输入目录中的所有文件
    local_paths = []
    for filename in os.listdir(input_directory):
        # 构建完整的文件路径
        flac_path = os.path.join(input_directory, filename)
        local_paths.append(flac_path)
        # 调用函数进行转换
    result_paths = audio_file_2_mp3(local_paths)
    copy_files_to_directory(result_paths, target_directory)


def copy_files_to_directory(file_paths, target_directory):
    """
        将文件复制到指定目录中
    """
    # 确保目标目录存在
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # 遍历文件路径列表并复制每个文件
    for file_path in file_paths:
        if os.path.isfile(file_path):
            # 获取文件名
            filename = os.path.basename(file_path)
            # 构建目标路径
            target_path = os.path.join(target_directory, filename)
            # 复制文件
            shutil.copy2(file_path, target_path)
            print(f"复制文件从: {file_path} 到 {target_path}")
        else:
            print(f"File not found: {file_path}")


if __name__ == '__main__':
    input_directory = r"D:\Personal\music\其他"
    target_directory = r"D:\Personal\music\MP3-其他"
    local_handle(input_directory, target_directory)
    