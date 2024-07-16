from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/ai_nav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    items = db.relationship('CategoryItem', backref='category', lazy=True)

class CategoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

# 创建数据库表
db.create_all()

# 添加类别及其项目
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    
    new_category = Category(key_name=data['key'], display_name=data['name'])
    db.session.add(new_category)
    db.session.flush()
    
    for item in data['list']:
        new_item = CategoryItem(name=item['name'], url=item['url'], category_id=new_category.id)
        db.session.add(new_item)
    
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'category_id': new_category.id}), 201

# 获取所有类别及其项目
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    
    for category in categories:
        items = [item for item in category.items]
        result.append({
            'id': category.id,
            'key': category.key_name,
            'name': category.display_name,
            'list': items
        })
    
    return jsonify(result)

# 更新类别及其项目
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    
    category.key_name = data['key']
    category.display_name = data['name']
    
    # 更新或添加项目
    for item in data['list']:
        existing_item = CategoryItem.query.filter_by(id=item['id']).first()
        if existing_item:
            existing_item.name = item['name']
            existing_item.url = item['url']
        else:
            new_item = CategoryItem(name=item['name'], url=item['url'], category_id=category.id)
            db.session.add(new_item)
    
    # 删除不存在于请求中的项目
    items_to_delete = [item for item in category.items if item.id not in [i['id'] for i in data['list']]]
    for item in items_to_delete:
        db.session.delete(item)
    
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'})

# 删除类别及其所有项目
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)