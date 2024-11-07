import os
from flask import Flask, render_template, request, jsonify, json, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv 
from datetime import datetime
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Create a SQLDatabaseChain to create and execute SQL queries
db = SQLDatabase.from_uri("mysql+pymysql://root:2021399346@localhost/clinic_db")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)
db = SQLAlchemy(app) 



class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20))
    initials = db.Column(db.String(3))
    sex = db.Column(db.String(1), nullable=False)
    address = db.Column(db.String(30))
    post_code = db.Column(db.String(6))
    admission = db.Column(db.Date)
    DOB = db.Column(db.Date, nullable=False)
    ward_id = db.Column(db.String(4))
    next_of_kin = db.Column(db.String(50))



class Ward(db.Model):
    __tablename__ = 'ward'
    ward_id = db.Column(db.String(4), primary_key=True)
    ward_name = db.Column(db.String(25))
    number_beds = db.Column(db.Integer, default=5)
    nurse_in_charge = db.Column(db.String(20), nullable=False)
    ward_type = db.Column(db.String(20))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route('/user-data', methods=['POST'])
def store_user_data():
    data = request.get_json()
    user = data.get('user')

    if user:
        session['user_data'] = user
        return jsonify({'message': 'User data stored successfully'}), 200
    else:
        return jsonify({'error': 'User data not provided'}), 400


@app.route('/dashboard')
def dashboard():
    user_data = session.get('user_data', None)
    current_year = datetime.now().year
    
    if user_data:
        return render_template('dashboard.html', user_data=user_data, current_year=current_year)
    else:
        return redirect(url_for('index'))


@app.route('/select_table', methods=['POST'])
def select_table():
    # Get the selected table from the form
    selected_table = request.form.get('table')
    
    if selected_table == 'patients':
        # Redirect to the patients route if 'Patients' is selected
        return redirect(url_for('patients'))
    elif selected_table == 'wards':
        # Redirect to the wards route if 'Wards' is selected
        return redirect(url_for('wards'))
    else:
        return render_template('dashboard.html', user_data=session.get('user_data', None), current_year=datetime.now().year)



@app.route('/patients')
def patients():
    # Fetch all patient records from the 'Patient' table
    patients = Patient.query.all()
    
    # Render the 'patients.html' template to display patient information
    return render_template('patients.html', patients=patients)

@app.route('/wards')
def wards():
    # Fetch all ward records from the 'Ward' table
    wards = Ward.query.all()
    
    # Render the 'wards.html' template to display ward information
    return render_template('wards.html', wards=wards)



@app.route('/add-ward', methods=['GET', 'POST'])
def add_ward():
    if request.method == 'POST':
        # Get the form data from the request
        ward_id = request.form['ward_id']
        ward_name = request.form['ward_name']
        number_beds = request.form['number_beds']
        nurse_in_charge = request.form['nurse_in_charge']
        ward_type = request.form['ward_type']

        # Example using SQLAlchemy:
        new_ward = Ward(ward_id=ward_id, ward_name=ward_name, number_beds=number_beds, nurse_in_charge=nurse_in_charge, ward_type=ward_type)
        db.session.add(new_ward)
        db.session.commit()

        # Redirect the user to the wards table page after successful insertion
        return redirect(url_for('wards'))

    return render_template('add-ward.html')



@app.route('/update-ward/<ward_id>', methods=['POST'])
def update_ward(ward_id):
    if request.method == 'POST':
        # Retrieve the edited ward data from the form
        ward_name = request.form.get('ward_name')
        number_beds = request.form.get('number_beds')
        nurse_in_charge = request.form.get('nurse_in_charge')
        ward_type = request.form.get('ward_type')

        # Retrieve the ward from the database
        ward = Ward.query.filter_by(ward_id=ward_id).first()

        if ward:
            # Update the ward data
            ward.ward_name = ward_name
            ward.number_beds = number_beds
            ward.nurse_in_charge = nurse_in_charge
            ward.ward_type = ward_type

            # Commit the changes to the database
            db.session.commit()

            # Redirect to the 'wards' route after the update
            return redirect(url_for('wards'))
        else:
            # Handle the case where the ward doesn't exist
            return "Ward not found", 404


@app.route('/edit-ward/<ward_id>')
def edit_ward(ward_id):
    ward = Ward.query.filter_by(ward_id=ward_id).first()

    if ward:
        return render_template('edit-ward.html', ward=ward)
    else:
        return "Ward not found", 404




@app.route('/add-patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Get the form data from the request
        patient_id = request.form['patient_id']
        name = request.form['name']
        initials = request.form['initials']
        sex = request.form['sex']
        address = request.form['address']
        post_code = request.form['post_code']
        admission_date = request.form['admission']
        date_of_birth = request.form['DOB']
        ward_id = request.form['ward_id']
        next_of_kin = request.form['next_of_kin']

        new_patient = Patient(patient_id=patient_id, name=name, initials=initials, sex=sex, address=address, post_code=post_code, admission=admission_date, DOB=date_of_birth, ward_id=ward_id, next_of_kin=next_of_kin)
        db.session.add(new_patient)
        db.session.commit()

        # Redirect the user to the patients table page after successful insertion
        return redirect(url_for('patients'))

    return render_template('add-patient.html')







@app.route('/edit-patient/<patient_id>')
def edit_patient(patient_id):
    # Retrieve the patient from the database based on 'patient_id'
    patient = Patient.query.filter_by(patient_id=patient_id).first()

    if patient:
        return render_template('edit-patient.html', patient=patient, patient_id=patient_id)
    else:
        return "Patient not found", 404


@app.route('/update-patient/<patient_id>', methods=['POST'])
def update_patient(patient_id):
    if request.method == 'POST':
        # Retrieve the edited patient data from the form
        name = request.form.get('name')

        # Retrieve the patient from the database
        patient = Patient.query.filter_by(patient_id=patient_id).first()

        if patient:
            # Update the patient data
            patient.name = name
            # Update other patient attributes

            # Commit the changes to the database
            db.session.commit()

            # Redirect to the patient list or any other appropriate page
            return redirect(url_for('patients'))
        else:
            # Handle the case where the patient doesn't exist
            return "Patient not found", 404


@app.route('/delete-patient/<patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if request.method == 'POST':
        # Retrieve the patient from the database
        patient = Patient.query.filter_by(patient_id=patient_id).first()

        if patient:
            # Delete the patient from the database
            db.session.delete(patient)
            db.session.commit()

            # Redirect to the patient list or any other appropriate page after deletion
            return redirect(url_for('patients'))
        else:
            # Handle the case where the patient doesn't exist
            return "Patient not found", 404





@app.route('/delete-ward/<ward_id>', methods=['POST'])
def delete_ward(ward_id):
    # Retrieve the ward from the database
    ward = Ward.query.filter_by(ward_id=ward_id).first()

    if ward:
        # Delete associated patients before deleting the ward
        patients_to_delete = Patient.query.filter_by(ward_id=ward_id).all()
        for patient in patients_to_delete:
            db.session.delete(patient)

        # Delete the ward itself
        db.session.delete(ward)

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the 'wards' route after the deletion
        return redirect(url_for('wards'))
    else:
        # Handle the case where the ward doesn't exist
        return "Ward not found", 404



@app.route('/chat')
def chat():
    # Render the chat.html template
    return render_template('chat.html')



@app.route('/get', methods=['POST'])
def get_bot_response():
    user_message = request.form['msg']

    # Assuming user_message is the LangChain function
    langchain_result = db_chain.run(user_message)

    return jsonify({'message': langchain_result})









if __name__ == "__main__":
    app.run(debug=True)
