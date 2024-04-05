from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')

@app.route('/forget')
def forget():
   return render_template('forget.html')

@app.route('/products')
def products():
    username= request.args.get('username')
    password= request.args.get('passsword')
    
    return render_template('products.html',username=username,password=password)

@app.route('/forget')
def product3():
    email2= request.args.get('email2')
    
    return render_template('forget.html',email2=email2)

@app.route('/products')
def products2():
    username2= request.args.get('username2')
    password2= request.args.get('passsword2')
    email = request.args.get('email')
    return render_template('products.html',username2=username2,password2=password2,email=email)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)