from datetime import datetime, timedelta
from flask import Flask, request, render_template, json, redirect, url_for, jsonify, session, send_file
import requests
import models.codeGen as uidGen
from models.modal import db, Library
from models.config import * 
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = Secret_Key

SESSION_TIMEOUT = 600 

with app.app_context():
    db.create_all()

@app.before_request
def update_last_activity():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=SESSION_TIMEOUT)
    session.modified = True
    session['last_activity'] = datetime.now()
    
def login_required(f):
    def wrapper(*args, **kwargs):
        update_last_activity()
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


def get_geolocation(ip_address):
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_time():
    now = datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return currentTime

DISCORD_WEBHOOK_URL = webHookAPIUrl

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form.get('code')
        if code in Secret_Code:
            session['logged_in'] = True
            
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                multip = request.environ['REMOTE_ADDR']

            else:
                multip = request.environ['HTTP_X_FORWARDED_FOR']

            ipSplit = multip.split(",")
            ip=ipSplit[0]
            
            location = get_geolocation(ip)
            if location["status"] == "fail": # type: ignore
                location_str = "Unknown"
                isp = "Unknown"
                cord = "Unknown"
            else:
                location_str = f"{location.get('city', 'Unknown')}, {location.get('regionName', 'Unknown')}, {location.get('country', 'Unknown')}" # type: ignore
                isp = location.get('isp', 'Unknown') # type: ignore
                cord = f"{location.get('lat', 'Unknown')}, {location.get('lon', 'Unknown')}" # type: ignore

            
            
            
            
            embed_content = {
                "title": "Login Details",
                "color": 5242879, 
                "thumbnail": {"url": "https://iili.io/JNsn2YF.jpg"}, 
                "fields": [
                    {"name": "IP", "value": ip, "inline": False},
                    {"name": "Location", "value": location_str, "inline": False},
                    {"name": "ISP", "value": isp, "inline": False},
                    {"name": "Coordinate", "value": cord, "inline": False},
                    {"name": "TimeStamp", "value": str(get_time()), "inline": False}
                ],
            }


            payload = {
                'embeds': [embed_content]
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

            if response.status_code == 204:
                print('Login Successful. Redirecting...')
            else:
                print('Failed to send login details to Discord.')
            return jsonify({'success': True, 'message': 'Login Successful. Redirecting...'})
        else:
            return jsonify({'success': False, 'error': 'Invalid code. Please try again.'})
    return render_template('login.html')

@app.route("/a")
def prasShortCut():
    return redirect(url_for("addBook"))

@app.route("/api/pras/book/db/add", methods=["GET", "POST"])
def addBook():
    if request.method == "POST":
        bookName = request.form.get("bookName")
        bookThumbnail = request.form.get("bookThumbnail")
        bookAuthor = request.form.get("bookAuthor")
        bookWebsite = request.form.get("bookWebsite")
        bookPublisher = request.form.get("bookPublisher")
        bookPublished = request.form.get("bookPublished")
        bookGenre = request.form.get("bookGenre")
        country = request.form.get("country")
        bookLang = request.form.get("bookLang")
        bookDesc = request.form.get("bookDesc")
        bookPage = request.form.get("bookPage")
        ebook = request.form.get("ebookLink")
        ISBN = request.form.get("ISBN")
        bookCharacter = request.form.get("bookChar")


        if not bookName:
            bookName = None
        if not bookThumbnail:
            bookThumbnail = None
        if not bookAuthor:
            bookAuthor = None
        if not bookWebsite:
            bookWebsite = None
        if not bookPublisher:
            bookPublisher = None
        if not bookPublished:
            bookPublished = None
        if not bookGenre:
            bookGenre = None
        if not country:
            country = "not available"
        if not bookLang:
            bookLang = None
        if not bookDesc:
            bookDesc = None
        if not bookPage:
            bookPage = None
        if not ebook:
            ebook = "not available"
        if not ISBN:
            ISBN = None
        if not bookCharacter:
            bookCharacter = "not available"


        add = Library(
            uid= f"prasX-{uidGen.UUIDGenerator()}",
            bookName=bookName,
            bookThumbnail=bookThumbnail,
            bookAuthor=bookAuthor,
            bookWebsite=bookWebsite,
            bookPublisher=bookPublisher,
            bookPublished=bookPublished,
            bookGenre=bookGenre,
            country=country,
            bookLang=bookLang,
            bookDesc=bookDesc,
            noOfPage=bookPage,
            eBook=ebook,
            isbn=ISBN,
            bookChar=bookCharacter,
        ) # type: ignore
    
        if add:
            db.session.add(add)
            db.session.commit()
            
            return jsonify({"success": True, "message": "Book added successfully to API!"})
        else:
            return jsonify({"success": False, "error": "Book adding process failed"}), 404


    if "logged_in" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))
        
DISCORD_WEBHOOK_URL_MAIL = webHookMAILUrl


@app.route("/api/doc", methods=["POST", "GET"])
@app.route("/api/docs", methods=["POST", "GET"])
@app.route("/api/documentation", methods=["POST", "GET"])
@app.route("/api/documentations", methods=["POST", "GET"])
def docs():
        if request.method == "POST":
            email = request.form.get('email')
            message = request.form.get('message')
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                multip = request.environ['REMOTE_ADDR']
            else:
                multip = request.environ['HTTP_X_FORWARDED_FOR']
            
            ipSplit = multip.split(",")
            ip = ipSplit[0]
            
            if email is not None:
                if "@gmail.com" in email:
                    thumb = "https://iili.io/JkgnpCF.png"
                elif "@outlook.com" in email or "@hotmail.com" in email:
                    thumb = "https://iili.io/JkgAOPI.png"
                elif any(domain in email for domain in ["@yahoo.com", "@yahoo.co.in", "@yahoo.ca", "@yahoo.com.au", "@yahoo.co.uk"]):
                    thumb = "https://iili.io/JkgAwnp.png"
                elif "@icloud.com" in email:
                    thumb = "https://iili.io/JkgAhtR.png"
                else:
                    thumb = "https://iili.io/JkgANMN.png"
            else:
                thumb = "https://iili.io/JkgANMN.png"
            
            mailcontent = {
                "title": "PrasMail",
                "color": 5242879, 
                "thumbnail": {"url": thumb}, 
                "fields": [
                    {"name": "From", "value": email, "inline": False},
                    {"name": "To", "value": "prassamin@gmail.com", "inline": False},
                    {"name": "Message", "value": message, "inline": False},
                    {"name": "IP", "value": ip, "inline": False},
                    {"name": "TimeStamp", "value": str(get_time()), "inline": False},
                    {"name": "Reply", "value": f"[Let's Go📨](https://prasbook.onrender.com/email/reply?reply={email})", "inline": False}
                ],
            }
            
            payload = {"embeds": [mailcontent]}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(DISCORD_WEBHOOK_URL_MAIL, json=payload, headers=headers)

            print(response.status_code)
            if response.status_code == 204:
                return jsonify({"success": True, "message": "Email sent successfully!"})
            else:
                return jsonify({"success": False, "error": "Failed to send email."})
    
        return render_template("docs.html")    
    
@app.route("/")
def index():
    return redirect(url_for("base"))

@app.route("/api")
def base():
    endPoints = {"EndPoints": {
        'all items': 'https://prasbook.onrender.com/api/books',
        'search': 'https://prasbook.onrender.com/api/books?q=<book name or author or genre or ISBN number or publisher or language>',
    },
    "WebPage": {
        'documentation': 'https://prasbook.onrender.com/api/docs',
    }
    }
    return app.response_class(
        response=json.dumps(endPoints, sort_keys=False),
        status=200,
        mimetype='application/json',
    )

@app.route("/email/reply")
def reply():
    send = request.args.get("reply")

    return render_template("reply.html", to=send)    

@app.route("/api/books", methods=["GET"])
def get_books():
    search_query = request.args.get('q')

    if search_query:
        
        if search_query.__contains__(". "):
            filterSearch = search_query.replace(". ", " ")
        elif search_query.__contains__(", "):
            filterSearch = search_query.replace(", ", " ")
        elif search_query.__contains__("."):
            filterSearch = search_query.replace(".", " ")
        elif search_query.__contains__("- "):
            filterSearch = search_query.replace("- ", " ")
        else:
            filterSearch = search_query
        
        search_terms = filterSearch.lower().split()
        filter_conditions = []

        for term in search_terms:
            filter_conditions.extend([
                Library.bookName.ilike(f"%{term}%"),
                Library.bookAuthor.ilike(f"%{term}%"),
                Library.bookGenre.ilike(f"%{term}%"),
                Library.bookLang.ilike(f"%{term}%"),
                Library.bookPublisher.ilike(f"%{term}%"),
                Library.isbn.ilike(f"%{term}%"),
            ])

        query = or_(*filter_conditions)
        books = Library.query.filter(query).all()
        found_count = len(books)

    else:
        books = Library.query.all()
        found_count = Library.query.count()


    books_data = [book.to_dict() for book in books]
    
    response_data = {
        "author": "PRAS",
        "available": found_count,
        "Books": books_data,
        
    }

    return app.response_class(
        response=json.dumps(response_data, sort_keys=False),
        status=200,
        mimetype='application/json'
    )

@app.route("/api/downloadDB")
def download():
    dbPath = "instance/library.db"
    return send_file(dbPath, as_attachment=True)


@app.route("/r")
def prasShortCut2():
    return redirect(url_for("removeBook"))

@app.route("/api/pras/book/db/remove", methods=["POST", "GET"])
def removeBook():
    if request.method == "POST":
        uid = request.form.get("uid")
        removeBook = Library.query.filter_by(uid=uid).first()
        if removeBook:
            db.session.delete(removeBook)
            db.session.commit()  

            return jsonify({"success": True, "message": "Book removed successfully from API!"})
        else:
            return jsonify({"success": False, "error": "Book not found"}), 404
    
    if "logged_in" in session:
        return render_template("remove.html")
    else:
        return redirect(url_for("login"))
    

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "error": "404 - Not Found"}), 404



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")