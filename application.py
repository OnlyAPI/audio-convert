env = {
    'path': {
        'upload': 'upload', # 上传文件存储路径
        'converted': 'converted' # 转换后文件存储路径,
    },
    'ffmpeg_path': {
        'Windows': {
            'ffmpeg': r"D:\Personal\ffmpeg-V2024-10-07\bin\ffmpeg.exe",
            'ffprobe': r"D:\Personal\ffmpeg-V2024-10-07\bin\ffprobe.exe"
        },
        'Linux': {
            'ffmpeg': r'',
            'ffprobe': r''
        },
        'Darwin': {
            'ffmpeg': r'',
            'ffprobe': r''
        }
    },
    'max_file_count': 10,
    'max_file_size': 50 * 1024 * 1024,
    'support_receive_audio_ext': {'mp3', 'wav', 'ogg', 'flac'}, # 允许转换的原音频格式
    'support_target_audio_ext': {'mp3', 'wav', 'ogg', 'flac'} # 允许转换的目标格式
}