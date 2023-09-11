from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Define the path to your Excel file
excel_file_path = 'questions.xlsx'

# Read data from the Excel sheet
def read_data():
    try:
        data = pd.read_excel(excel_file_path, sheet_name='questions')
        return data.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading data from Excel: {e}")
        return []

# Define a route for the home page (root URL '/')
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for the admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Define a route for generating unique URLs and redirecting to "skill test"
@app.route('/generate_url', methods=['POST'])
def generate_url():
    name = request.form['name']
    job_role = request.form['job_role']
    years_of_experience = request.form['years_of_experience']

    # Generate a unique URL for the candidate that redirects to "skill test"
    unique_url = f'/skill-test/{name}-{job_role}-{years_of_experience}'

    # Redirect to the generated URL
    return redirect(unique_url)

# Define a route for the "skill test" page
@app.route('/skill-test/<candidate_info>', methods=['GET', 'POST'])
def skill_test(candidate_info):
    # Extract candidate information from the URL (you can parse it as needed)
    candidate_info_parts = candidate_info.split('-')
    name = candidate_info_parts[0]
    job_role = candidate_info_parts[1]
    years_of_experience = candidate_info_parts[2]

    # Retrieve questions from the Excel file
    questions = read_data()

    # Handle form submission for the skill test (evaluate answers)
    if request.method == 'POST':
        # Get and process submitted answers here
        # You can access form data using request.form

        # For example, you can collect selected options for each question
        selected_options = {}
        for question in questions:
            selected_option_key = f'question_{question["id"]}'
            selected_option_id = int(request.form.get(selected_option_key))
            selected_options[question["id"]] = selected_option_id

        # Implement your logic to evaluate answers and calculate the score
        # For demonstration purposes, calculate a mock score here (you should replace this logic)
        score = calculate_mock_score(selected_options)

        # You can store the score in a database or perform other actions here

        return render_template('results.html', name=name, job_role=job_role, years_of_experience=years_of_experience, score=score)

    # Render the "skill test" page with candidate information and questions
    return render_template('skill_test.html', name=name, job_role=job_role, years_of_experience=years_of_experience, questions=questions)

# Define a route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    # Perform authentication logic here (e.g., check username and password against a database)

    # For this example, let's assume successful authentication
    authentication_successful = True

    # If authentication is successful, redirect to the admin page
    if authentication_successful:
        return redirect(url_for('admin'))

    # If authentication fails, return an error message or redirect to the login page with a message
    return render_template('index.html', error_message='Login failed')

# Define a success route (you can customize this)
@app.route('/success')
def success():
    return "Login successful!"

def calculate_mock_score(selected_options):
    # Replace this mock scoring logic with your actual scoring logic
    # Here, we assume that correct answers have option IDs 1, 3, 5, etc.
    correct_option_ids = set(range(1, len(selected_options) * 2, 2))
    user_selected_option_ids = set(selected_options.values())
    correct_count = len(correct_option_ids.intersection(user_selected_option_ids))
    total_questions = len(selected_options)
    score_percentage = (correct_count / total_questions) * 100
    return score_percentage

if __name__ == '__main__':
    app.run(debug=True)
