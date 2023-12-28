from flask import Flask, render_template, request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Category('{self.name}')"
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_no = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='products')
def __repr__(self):
        return f"Product('{self.product_no}', '{self.description}', '{self.price}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return f"Category('{self.name}')"    

db.create_all()

clothing_category = Category(name='Clothing')
db.session.add(clothing_category)
db.session.commit()

products = [
    {'product_no': '123', 'description': 'Shirt', 'price': 162.95, 'image': 'armonikagömlek.png'},
    {'product_no': '1231', 'description': 'Shirt', 'price': 440, 'image': 'Trendnakış.png'},
    {'product_no': '1232', 'description': 'Shirt', 'price': 169, 'image': 'arm.png'},
    {'product_no': '1233', 'description': 'Shirt', 'price': 2925, 'image': 'guitar_yor.png'},
    {'product_no': '1234', 'description': 'Shirt', 'price': 159, 'image': 'hakke.png'},
    {'product_no': '1235', 'description': 'Shirt', 'price': 264, 'image': 'son.png'},
    {'product_no': '124', 'description': 'Pajama', 'price': 185.91, 'image': 'siyah inci.png'},
    {'product_no': '125', 'description': 'Leggings', 'price': 193.99, 'image': 'armonika.png'},
    {'product_no': '126', 'description': 'Sweater', 'price': 145 , 'image': 'kadınpolo.png'},
    {'product_no': '127', 'description': 'Pants', 'price': 249.99, 'image': 'fvpantolon.png'},
]

for product_data in products:
    product = Product(
        product_no=product_data['product_no'],
        description=product_data['description'],
        price=product_data['price'],
        image=product_data['image'],
        category=clothing_category 
    )
    db.session.add(product)
db.session.commit()

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/search', methods=['POST'])
def search():
     if request.method == 'POST':
        search_term = request.form.get('search')
        results = Product.query.filter(
            (Product.product_no.like(f'%{search_term}%')) |
            (Product.description.like(f'%{search_term}%')) |
            (Product.category.like(f'%{search_term}%'))
        ).all()
        return render_template('search_results.html', results=results, search_term=search_term)
    

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)