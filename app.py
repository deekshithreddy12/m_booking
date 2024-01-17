from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_ticket_booking.db'
db = SQLAlchemy(app)


# Define User entity
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# Define Movie entity
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    cast = db.Column(db.String(255))

# Define Cinema entity
class Cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)

# Define Showtime entity
class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    timing = db.Column(db.DateTime, nullable=False)

# Define Seat entity
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

# Define Payment entity
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')

# Define Review entity
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)

# Define Booking entity
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')




@app.route("/")
def helloworld():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify({'users': user_list})


@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    new_movie = Movie(**data)
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'Movie created successfully'}), 201

# Example: Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = [{'title': movie.title, 'genre': movie.genre, 'duration': movie.duration, 'cast': movie.cast} for movie in movies]
    return jsonify({'movies': movie_list})

@app.route('/cinemas', methods=['POST'])
def create_cinema():
    data = request.json
    new_cinema = Cinema(**data)
    db.session.add(new_cinema)
    db.session.commit()
    return jsonify({'message': 'Cinema created successfully'}), 201

@app.route('/cinemas', methods=['GET'])
def get_cinemas():
    cinemas = Cinema.query.all()
    cinema_list = [{'name': cinema.name, 'location': cinema.location} for cinema in cinemas]
    return jsonify({'cinemas': cinema_list})

# CRUD operations for Showtime
@app.route('/showtimes', methods=['POST'])
def create_showtime():
    data = request.json
    new_showtime = Showtime(**data)
    db.session.add(new_showtime)
    db.session.commit()
    return jsonify({'message': 'Showtime created successfully'}), 201

@app.route('/showtimes', methods=['GET'])
def get_showtimes():
    showtimes = Showtime.query.all()
    showtime_list = [{'movie_id': showtime.movie_id, 'cinema_id': showtime.cinema_id, 'timing': showtime.timing} for showtime in showtimes]
    return jsonify({'showtimes': showtime_list})

# CRUD operations for Seat
@app.route('/seats', methods=['POST'])
def create_seat():
    data = request.json
    new_seat = Seat(**data)
    db.session.add(new_seat)
    db.session.commit()
    return jsonify({'message': 'Seat created successfully'}), 201

@app.route('/seats', methods=['GET'])
def get_seats():
    seats = Seat.query.all()
    seat_list = [{'cinema_id': seat.cinema_id, 'number': seat.number, 'is_available': seat.is_available} for seat in seats]
    return jsonify({'seats': seat_list})

# CRUD operations for Payment
@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully'}), 201

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    payment_list = [{'user_id': payment.user_id, 'amount': payment.amount, 'status': payment.status} for payment in payments]
    return jsonify({'payments': payment_list})

# CRUD operations for Review
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully'}), 201

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = [{'user_id': review.user_id, 'movie_id': review.movie_id, 'rating': review.rating, 'comment': review.comment} for review in reviews]
    return jsonify({'reviews': review_list})

if __name__ == '__main__':
    with app.app_context():
        
        
        db.create_all()
    app.run(debug=True)


