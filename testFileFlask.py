import http.server
import socketserver
import os
 
# 定义一个处理请求的类，继承自BaseHTTPRequestHandler
class BlobPngHandler(http.server.BaseHTTPRequestHandler):
    
    # 处理GET请求的方法
    def do_GET(self):
        # 指定图片文件的路径
        image_path = 'image/猫21.png'
        
        # 打开图片文件，以二进制方式读取
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        # 设置响应的Content-Type头部
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        
        # 发送图片数据
        self.wfile.write(image_data)
 
# 创建服务器实例
def run(server_class=http.server.HTTPServer, handler_class=BlobPngHandler):
    server_address = ('localhost', 8000)  # 服务器地址和端口
    httpd = server_class(server_address, handler_class)
    print('服务器运行在 http://localhost:8000/')
    httpd.serve_forever()
 
# 运行服务器
if __name__ == '__main__':
    run()