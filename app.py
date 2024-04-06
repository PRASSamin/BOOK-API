from datetime import datetime, timedelta
from flask import Flask, request, render_template, json, redirect, url_for, jsonify, session
import requests
import modals.codeGen as uidGen
from modals.modal import db, Library
from modals.config import * 
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = Secret_Key

SESSION_TIMEOUT = 600 


with app.app_context():
    db.create_all()
    
def check_session_timeout():
    if 'last_activity' in session:
        last_activity_time = session['last_activity']
        current_time = datetime.now()
        if (current_time - last_activity_time).total_seconds() > SESSION_TIMEOUT:
            session.pop('logged_in', None)
            session.pop('last_activity', None)

@app.before_request
def update_last_activity():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=SESSION_TIMEOUT)
    session.modified = True
    session['last_activity'] = datetime.now()

    
def login_required(f):
    def wrapper(*args, **kwargs):
        check_session_timeout()
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


# Your Discord webhook URL
DISCORD_WEBHOOK_URL = webHookUrl


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form.get('code')
        if code in Secret_Code:
            session['logged_in'] = True
            # ip = request.remote_addr
            ip = '103.137.108.14' 
            location = get_geolocation(ip)
            if location["status"] == "fail":
                location_str = "Unknown"
                isp = "Unknown"
                cord = "Unknown"
            else:
                location_str = f"{location.get('city', 'Unknown')}, {location.get('regionName', 'Unknown')}, {location.get('country', 'Unknown')}"
                isp = location.get('isp', 'Unknown')
                cord = f"{location.get('lat', 'Unknown')}, {location.get('lon', 'Unknown')}"

            
            
            
            
            # Prepare rich embed content
            embed_content = {
                "title": "Login Details",
                "color": 5242879,  # White color
                "thumbnail": {"url": "https://iili.io/JNsn2YF.jpg"},  # Thumbnail image (small)
                "fields": [
                    {"name": "IP", "value": ip, "inline": False},
                    {"name": "Location", "value": location_str, "inline": False},
                    {"name": "ISP", "value": isp, "inline": False},
                    {"name": "Coordinate", "value": cord, "inline": False},
                    {"name": "TimeStamp", "value": str(get_time()), "inline": False}
                ],
            }


            # Send message to Discord
            payload = {
                'embeds': [embed_content]
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

            if response.status_code == 200:
                print('Login Successful. Redirecting...')
            else:
                print('Failed to send login details to Discord.')
            return jsonify({'success': True, 'message': 'Login Successful. Redirecting...'})
        else:
            return jsonify({'success': False, 'error': 'Invalid code. Please try again.'})
    return render_template('login.html')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bookName = request.form.get("bookName")
        bookThumbnail = request.form.get("bookThumbnail")
        bookAuthor = request.form.get("bookAuthor")
        sLink = request.form.get("sLink")
        bookWebsite = request.form.get("bookWebsite")
        bookPublisher = request.form.get("bookPublisher")
        bookPublished = request.form.get("bookPublished")
        bookGenre = request.form.get("bookGenre")
        country = request.form.get("country")
        bookLang = request.form.get("bookLang")
        bookDesc = request.form.get("bookDesc")

        if not bookName:
            bookName = None
        if not bookThumbnail:
            bookThumbnail = None
        if not bookAuthor:
            bookAuthor = None
        if not sLink:
            sLink = None
        if not bookWebsite:
            bookWebsite = None
        if not bookPublisher:
            bookPublisher = None
        if not bookPublished:
            bookPublished = None
        if not bookGenre:
            bookGenre = None
        if not country:
            country = None
        if not bookLang:
            bookLang = None
        if not bookDesc:
            bookDesc = None

        add = Library(
            uid= f"prasX-{uidGen.UUIDGenerator()}",
            bookName=bookName,
            bookThumbnail=bookThumbnail,
            bookAuthor=bookAuthor,
            sLink=sLink,
            bookWebsite=bookWebsite,
            bookPublisher=bookPublisher,
            bookPublished=bookPublished,
            bookGenre=bookGenre,
            country=country,
            bookLang=bookLang,
            bookDesc=bookDesc
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
                Library.bookGenre.ilike(f"%{term}%")
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




@app.route("/remove", methods=["POST", "GET"])
def remove():
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
    app.run(debug=False)