import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from subprocess import run

def build_docs():
    """构建文档"""
    # 确保在docs目录下
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 构建HTML文档
    result = run(['make', 'html'], capture_output=True, text=True)
    if result.returncode != 0:
        print("构建文档失败:")
        print(result.stderr)
        sys.exit(1)

    print("文档构建成功!")

def serve_docs():
    """启动HTTP服务器"""
    os.chdir('_build/html')

    # 配置服务器
    PORT = 8000
    server = HTTPServer(('', PORT), SimpleHTTPRequestHandler)

    # 打开浏览器
    webbrowser.open(f'http://localhost:{PORT}')

    print(f"文档服务已启动: http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n停止服务器...")
        server.shutdown()

if __name__ == '__main__':
    build_docs()
    serve_docs()
