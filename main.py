from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = "123456"  # Put in environment variable
Bootstrap(app)

# Configure Cafes database
# Connect to database (in project directory)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
debug = True  # Remove for production

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)  # British pounds

    def to_dict(self):
        """Convert data record fields to dictionary using comprehension"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Configure Cafe Input Form
class CafeForm(FlaskForm):
    name         = StringField('Cafe Name', validators=[DataRequired()])
    map_url      = StringField("Cafe Location on Apple/Google Maps (URL)", validators=[DataRequired()])
    img_url      = StringField("Cafe Image (URL)", validators=[DataRequired()])
    location     = StringField("City/Town Name", validators=[DataRequired()])
    has_sockets  = SelectField("Has Sockets", choices=["Yes", "No"])
    has_toilet   = SelectField("Has Toilet", choices=["Yes", "No"])
    has_wifi     = SelectField("Has WiFi", choices=["Yes", "No"])
    take_calls   = SelectField("Can Take Calls", choices=["Yes", "No"])
    seats        = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit       = SubmitField("Add Cafe")

# Open index.html
@app.route("/")
def home():
    return render_template("index.html")


# Display cafes table
@app.route('/cafes')
def cafes():
    """Returns all cafes"""

    all_cafes = db.session.query(Cafe).all() # Get all cafes in database
    return render_template("cafes.html", cafes=all_cafes)


# Create Add Cafe page
@app.route('/add', methods=["GET", "POST"])
def add():
    """Add new cafe to database"""

    form = CafeForm()

    if request.method == "POST":

        if form.validate_on_submit():

            # Get new cafe fields from CafeForm
            cafe_name = form.name.data
            cafe_map_url = form.map_url.data
            cafe_img_url = form.img_url.data
            cafe_location = form.location.data
            cafe_sockets = form.has_sockets.data
            cafe_toilet = form.has_toilet.data
            cafe_wifi = form.has_wifi.data
            cafe_take_calls = form.take_calls.data
            cafe_seats = form.seats.data
            cafe_coffee_price = form.coffee_price.data

            if debug:
                print(
                    f"\ncafe_name         = {cafe_name},"
                    f"\ncafe_map_url      = {cafe_map_url},"
                    f"\ncafe_img_url      = {cafe_img_url},"
                    f"\ncafe_location     = {cafe_location},"
                    f"\ncafe_sockets      = {cafe_sockets},"
                    f"\ncafe_toilet       = {cafe_toilet},"
                    f"\ncafe_wifi         = {cafe_wifi},"
                    f"\ncafe_take_calls   = {cafe_take_calls},"
                    f"\ncafe_seats        = {cafe_seats},"
                    f"\ncafe_coffee_price = {cafe_coffee_price}\n"
                )

            # Append to cafes.db database
            # TODO: Shorten map and img urls automagically before saving
            new_cafe = Cafe (
                name=cafe_name,
                map_url = cafe_map_url,
                img_url = cafe_img_url,
                location = cafe_location,
                has_sockets = True if cafe_sockets == "Yes" else False,
                has_toilet = True if cafe_toilet == "Yes" else False,
                has_wifi = True if cafe_wifi == "Yes" else False,
                can_take_calls = True if cafe_take_calls == "Yes" else False,
                seats = cafe_seats,
                coffee_price = cafe_coffee_price
            )
            db.session.add(new_cafe)
            db.session.commit()

            return redirect(url_for('cafes'))  # Show all cafes

    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
