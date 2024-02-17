from model import *
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'QWJhaWt1bWFyIEk='
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def start():
    if session is None and session['username']:
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/home')
def home():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("home.html")

@app.route('/home1')
def home1():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("home1.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if session is None and session['username']:
        return redirect(url_for('home'))
    elif request.method == "GET":
        return render_template("signup.html", msg=None, mail="", pwd="")
    else:
        if  request.form['user_type'] == "customer":
            if data.createAccountc(request.form["mail"], request.form["password"]):
                return redirect(url_for('login'))
            else:
                return render_template("signup.html", msg="Account already exists", mail=request.form["mail"], pwd=request.form["password"])
        else:
                if data.createAccounta(request.form["mail"], request.form["password"]):
                    return redirect(url_for('login'))
                else:
                    return render_template("signup.html", msg="Account already exists", mail=request.form["mail"], pwd=request.form["password"])
        


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session is None and session['username']:
            return redirect(url_for('home'))
        return render_template("login.html", msg=None, mail="", pwd="")
    else:
        if data.loginAccount(request.form["mail"], request.form["password"]) == 1:
            session['username'] = request.form["mail"]
            session['type']='c'
            return redirect(url_for('home'))
        if data.loginAccount(request.form["mail"], request.form["password"]) == 2:
            session['username'] = request.form["mail"]
            session['type']='a'
            return redirect(url_for('home1'))
        else:
            return render_template("login.html", msg="Invalid User or Password", mail=request.form["mail"], pwd=request.form["password"])


@app.route('/logout')
def logout():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/addItem", methods=["GET"])
def addItem():
    if session and session['username']:
        itemID = request.args.get("itemID")
        if data.addItemToCart(itemID, session["username"]):
            return jsonify({"result": True})
    return jsonify({"result": False})


@app.route('/checkout')
def checkout():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("checkout.html")


@app.route('/getCheckoutList')
def getCheckoutList():
    if session is None or session.get('username') is None:
        return jsonify({"msg": False})
    return jsonify(data.getItemFromCart(session.get('username')))


@app.route('/singlePage')
def singlePage():
    product_id = request.args.get('pid')
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("product_details.html", pid=product_id)

@app.route('/art_detail')
def art_detail():
    return render_template("add_artist_details.html")


@app.route('/ar_add')
def ar_add():
    return render_template("artadd.html")

@app.route('/contact')
def contact():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/addArtist')
def addArtist():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('add_artist_details.html')


@app.route('/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)


@app.route('/uploads/<path:filename>')
def getImage(filename):
    print(filename)
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return send_from_directory("uploads", filename)


@app.route('/get_data', methods=['GET'])
def get_data():
    page = request.args.get("pageno")
    record = data.getData(int(page))
    if record[0]:
        return jsonify({'status': 'success', 'data': record[1]})
    else:
        return jsonify({'status': 'error', 'data': "Error"})

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        profile_image = request.files['profile_image']
        skills = request.form['skills']
        certificates = request.files.getlist('certificates')
        sign_image = request.files['sign_image']
        phone_number = request.form['phone_number']
        address = request.form['address']
        country = request.form['country']
        masterpiece = request.files['masterpiece']

        # Save uploaded files
        profile_file_name = save_file(profile_image, 'profile')
        sign_file_name = save_file(sign_image, 'signature')
        certificate_file_names = [save_file(cert, f'certificate{i+1}') for i, cert in enumerate(certificates)]
        masterpiece_file_name = save_file(masterpiece, 'masterpiece')

        # Store data in MongoDB
        artist_details = {
            'profile_image': profile_file_name,
            'skills': skills,
            'certificates': certificate_file_names,
            'sign_image': sign_file_name,
            'phone_number': phone_number,
            'address': address,
            'country': country,
            'masterpiece': masterpiece_file_name,
            'timestamp': datetime.now()
        }
        if(data.addartist(artist_details, session["username"])==True):
            return render_template("home1.html")
        else:
            return render_template("add_artist_details.html", msg="not")
        

def save_file(file, filename):
    if file:
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        file_id = session["username"] +"_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_file_name = f'{filename}_{file_id}.{file_extension}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
        file.save(file_path)
        return new_file_name
    return None 
  
@app.route('/get_single_product', methods=['GET'])
def get_single_product():
    record = data.getSingle(request.args.get("pid"))
    if record[0]:
        return jsonify({'status': 'success', 'data': record[1]})
    else:
        return jsonify({'status': 'error', 'data': "Error"})

@app.route('/setCheckoutData', methods=['POST'])
def setCheckoutData():
    if request.method == "POST":
        record = request.json
        record = record.get('data')
        if data.updateCheckoutData(record, session.get("username")):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
    return jsonify({'status': 'error'})

@app.route("/ar",methods=['POST'])
def ar():
    if request.method == 'POST':
        print("POSTER")
        title = request.form['title']
        des = request.form['description']
        art_file = request.files.getlist('artpieceimage')
        sell_type = request.form['sell_type']
        price = request.form['price']
        art_file_names = []
        for i, cert in enumerate(art_file):
            art_file_names.append(save_file(cert, f'art{i+1}'))

        artist_details = {
            'title': title,
            'des':des,
            'art': art_file_names,
            'sell_type': sell_type,
            'price': price,
            'user':session['username'],
            "discount": 1,
        }

        if(data.ar(artist_details)==True):
            return render_template("home1.html")
        else:
            return render_template("productadd.html")

from nltk.corpus import wordnet as wn
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["Art_Gallery"]
productCollection = database["Products"]

def jaccard_similarity(str1, str2):
    set1 = set(str1.lower())
    set2 = set(str2.lower())
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union if union else 0

def sort_art_titles_by_meaning(art_titles, keyword):
    similarity_scores = [(title, jaccard_similarity(keyword, title)) for title in art_titles]
    sorted_art_titles = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    return [title for title, _ in sorted_art_titles]

def similarity(keyword):
    titles_cursor = productCollection.find({}, {'_id': 0, 'title': 1})
    art_titles = []

    # Extract and print each title
    for product in titles_cursor:
        art_titles.append(product['title'])
    sorted_titles = sort_art_titles_by_meaning(art_titles, keyword)
    return sorted_titles[:5]

@app.route("/getKeyword", methods=["GET"])
def getKeyword():
    if request.method == 'GET':
        print(request.args.get("word"))
        return jsonify({"data" : similarity(request.args.get("word"))})
    
if __name__ == "__main__":
    app.run(debug=True)
