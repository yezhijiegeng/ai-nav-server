from flask import Flask, request, jsonify
import mysql.connector

from flask_cors import cross_origin # 未特定路由启用cors
from flask_cors import CORS   # 全局允许跨域请求
app = Flask(__name__)
CORS(app)  # 全局允许跨域请求



# 配置数据库连接
config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'ai_nav'
}

# 连接数据库
def db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print(e)
    return conn

# 定义CRUD操作的路由
# @app.route('/add', methods=['POST'])
# def add():
#     # 获取请求数据并添加到数据库
#     # ...
#     return jsonify({'message': 'Added successfully'})



@app.route('/update', methods=['PUT'])
def update():
    # 更新数据库中的记录
    # ...
    return jsonify({'message': 'Updated successfully'})

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    # 从数据库中删除记录
    # ...
    return jsonify({'message': 'Deleted successfully'})

@app.route('/get/<id>', methods=['GET'])
def get(id):
    # 从数据库中获取记录
    # ...
    return jsonify(record)

@app.route('/get_all', methods=['GET'])
@cross_origin(origins="http://127.0.0.1:5174")  # 这将为这个路由启用CORS
def get_all():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")  # 假设你的表名为items
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # 将查询结果转换为JSON格式
    products = [{'id': row[0], 'name': row[1]} for row in rows]
    
    return jsonify(products)

@app.route('/get_nav_list', methods=['GET'])
@cross_origin(origins="http://localhost:5174")  # 这将为这个路由启用CORS
def get_nav_list():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM nav_list")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # 将查询结果转换为 JSON 格式
    result = [dict(row) for row in rows]
    return jsonify(result)

""" @app.route('/add_nav', methods=['POST'])
@cross_origin(origins="http://localhost:5174")  # 这将为这个路由启用CORS
def add_nav():
    print("add_nav")
    name = request.form['name'].get()
    type = request.form['type'].strip()
    list = request.form['list'].strip()
    try:
        conn = mysql.connector.connect(**config)
        with conn.cursor() as cursor:
            sql = "INSERT INTO `nav_list` (`name`, `type`,`list`) VALUES (%s, %s,%s)"
            cursor.execute(sql, (name, type,list))
            rows = cursor.fetchall()
            cursor.close()
            result = [dict(row) for row in rows]
            return jsonify(result)
    except Exception as e:
        cursor.close()
        print(e) """

# 增加一条数据
@app.route("/add_nav", methods=['POST'])
@cross_origin(origins="http://localhost:5174") 
def add_nav():
    id = request.form.get("id")
    name = request.form.get("name")
    list = request.form.get("list")
    type = request.form.get("type")

    if not id or not name or not list or not list:
        return jsonify({"message": "缺少必填参数"}), 400

    try:
        query = "insert into nav_list (id, name, list, type) values (%s,%s, %s, %s)"
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id,name, list,type))
        conn.commit()
        return jsonify({"message": f"{name}新增成功"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)