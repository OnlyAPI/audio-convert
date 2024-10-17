import waitress
from app import app  # 导入你的 Flask 应用实例

if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=8081)
