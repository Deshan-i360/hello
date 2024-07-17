# Import necessary libraries and functions
from flask import Flask, jsonify, request
from transformers import pipeline
import pandas as pd

# Initialize the summarization pipeline with a specified model
summarizer = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

# Sample text to be summarized
text = "If you're a little more tech savvy, you could also use your Mac's Terminal window. Using this method, you can search both your Mac's private and public IP addresses"

# Load the CSV files into DataFrames
dosageform = pd.read_csv('dosageform.csv')
medicine_df = pd.read_csv('medicine.csv')
manufacturer = pd.read_csv('manufacturer.csv')
indication = pd.read_csv('indication.csv')
generic = pd.read_csv('generic.csv')
drugclass = pd.read_csv('drugclass.csv')

# Create a Flask app
app = Flask(__name__)


# In-memory storage for prescriptions
prescriptions = []


# Home route for testing (GET and POST methods)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Generate a summary of the sample text
        data = summarizer(text, max_length=21)
        return jsonify({'data': data})

# Route to summarize text sent via POST request
@app.route('/summarize', methods=['POST'])
def summarize_text():
    if request.is_json:
        data = request.get_json()  # Get JSON data from the request
        if 'text' in data:
            text = data['text']
            # Summarize the text using the pipeline
            summary = summarizer(text, max_length=20, min_length=20, do_sample=False)
            return jsonify({'summary': summary[0]['summary_text']})
        else:
            return jsonify({'error': 'No text provided in the request'}), 400
    else:
        return jsonify({'error': 'Request should be in JSON format'}), 400

# Route to calculate the square of a number (GET method)
@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    return jsonify({'data': num**2})

# Route to get data from the medicine DataFrame
@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicine_names = [medicine['brand name'] for medicine in medicine_df.to_dict(orient='records')]
    return jsonify(medicine_names)

# Route to get data from the manufacturer DataFrame
@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    manufacturers = manufacturer.to_dict(orient='records')
    return jsonify(manufacturers)

# Route to get data from the indication DataFrame
@app.route('/indications', methods=['GET'])
def get_indications():
    indications = indication.to_dict(orient='records')
    return jsonify(indications)

# Route to get data from the drug class DataFrame
@app.route('/drugclasses', methods=['GET'])
def get_drugclasses():
    drugclasses = drugclass.to_dict(orient='records')
    return jsonify(drugclasses)

# Route to get data from the dosage form DataFrame
@app.route('/dosageforms', methods=['GET'])
def get_dosageforms():
    dosage_form_names = [form['dosage form name'] for form in dosageform.to_dict(orient='records')]
    return jsonify(dosage_form_names)


# Route to post a new prescription
@app.route('/api/prescription', methods=['POST'])
def post_prescription():
    if request.is_json:
        data = request.get_json()
        if 'patient' in data and 'medicines' in data:
            prescription = {
                'id': len(prescriptions) + 1,
                'patient': data['patient'],
                'medicines': data['medicines']
            }
            prescriptions.append(prescription)
            return jsonify({'message': 'Prescription posted successfully', 'prescription': prescription}), 201
        else:
            return jsonify({'error': 'Missing doctorName or imageUrl'}), 400
    else:
        return jsonify({'error': 'Request should be in JSON format'}), 400

# Route to fetch all prescriptions
@app.route('/api/prescriptions', methods=['GET'])
def fetch_prescriptions():
    return jsonify(prescriptions)




# Driver function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
