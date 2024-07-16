import http.server
import socketserver
import urllib.parse
import os
 
# 处理请求的类
class SimpleHTTPRequestHandlerWithFileStream(http.server.SimpleHTTPRequestHandler):
    
    # 重写do_GET方法来处理GET请求
    def do_GET(self):
        # 解析URL参数
        parsed_path = urllib.parse.urlparse(self.path)
        query_components = urllib.parse.parse_qs(parsed_path.query)
        
        # 检查是否有正确的path参数
        if 'path' in query_components:
            file_path = query_components['path'][0]
            
            # 确保文件存在且是PNG文件
            if os.path.isfile(file_path) and file_path.endswith('.png'):
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                
                # 发送文件内容
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
                return
        
        # 如果没有正确的参数或文件不存在，返回404
        self.send_error(404, 'File not found')
 
def run(server_class=socketserver.TCPServer, handler_class=SimpleHTTPRequestHandlerWithFileStream):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    
    print('Serving at http://localhost:8000')
    httpd.serve_forever()
 
if __name__ == '__main__':
    run()