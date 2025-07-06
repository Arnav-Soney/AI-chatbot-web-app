from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    print(f"Current directory: {os.getcwd()}")
    print(f"Templates exist: {os.path.exists('templates')}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)