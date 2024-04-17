from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    contributors = {
        'Brennan': 'Developer',
        'Micheal': 'Developer',
        'Nathan': 'Developer',
        'Daniela': 'Developer',
        # Add more contributors and roles here
    }
    tasks = {
        'Task 1': 'Brennan',
        'Task 2': 'Micheal',
        'Task 3': 'Daniela',
        # Add more tasks and assignees here
    }
    return render_template('HomePage.html', contributors=contributors, tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
