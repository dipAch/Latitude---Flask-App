from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

# Connect to the Database.
# DB Connection string below.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/learningflask'

# Initialize the Flask App to use the SQLAlchemy ORM to communicate
# to the DB.
db.init_app(app)

# Protection against CSRF.
app.secret_key = 'development-key'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	# Check for GET / POST Requests.
	if request.method == 'POST':
		if not form.validate():
			return render_template('signup.html', form=form)

		# Form has valid data, so persist to the Database.
		new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
		db.session.add(new_user)
		db.session.commit()

		# Start User Session.
		session['email'] = new_user.email
		return redirect(url_for('home'))
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
	if 'email' not in session:
		return redirect(url_for('login'))

	form = AddressForm()

	places = []
	my_coordinates = (37.4221, -122.0844)

	if request.method == 'POST':
		if not form.validate():
			return render_template('home.html', form=form)

		# Handle the Form here.
		# Get the adress.
		address = form.address.data

		# Query for places around it.
		p = Place()
		my_coordinates = p.address_to_latlng(address)
		places = p.query(address)

		# Return those results.
		return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)
	elif request.method == 'GET':
		return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	# Check for GET / POST Requests.
	if request.method == 'POST':
		if not form.validate():
			return render_template('login.html', form=form)

		# Get the relevant form fields.
		email    = form.email.data
		password = form.password.data

		# Retrieve User Information.
		user = User.query.filter_by(email=email).first()

		if user is not None and user.check_password(password):
			session['email'] = user.email
			return redirect(url_for('home'))

		# Redirect to the Login Page.
		return redirect(url_for('login'))
	elif request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)