from flask import Flask, request, jsonify
import mysql.connector

from flask_cors import cross_origin  # 未特定路由启用cors
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
    data = request.get_json()  # 获取JSON数据
    print("data", data)
    """ name = request.form.get("name")
    type = request.form.get("type") """
    print('-------------------')
    name = data.get("name")
    type = data.get("type")
    print(name, type)

    if not name or not type:
        return jsonify({"message": "缺少必填参数"}), 400

    try:
        query = "insert into nav_list (name, type) values (%s,%s)"
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (name, type))
        conn.commit()
        return jsonify({"message": f"{name}新增成功", "code": 200}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

    
# 修改某条数据
@app.route("/update_nav/<int:id>", methods=['PUT'])
@cross_origin(origins="http://localhost:5174")
def update_nav(id):

    data = request.get_json()  # 获取JSON数据
    name = data.get("name")
    type = data.get("type")

    if not name and not type:
        return jsonify({"message": "缺少必要参数"}), 400

    update_query = "update nav_list set "
    update_params = []

    if name:
        update_query += "name=%s, "
        update_params.append(name)
    if type:
        update_query += "type=%s, "
        update_params.append(type)

    update_query = update_query.rstrip(', ')

    query = f"{update_query} where id=%s"
    update_params.append(id)
    # print(query)
    # print(update_params)
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(update_params))
        conn.commit()
        return jsonify({"message": f"学生{name}信息更新成功", "code": 200}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# 删除某条数据
@app.route("/delete_nav/<int:id>", methods=['DELETE'])
def delete_nav(id):
    query = "delete from nav_list where id=%s"
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"message": f"分类 {id} 删除成功", "code": 200}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
