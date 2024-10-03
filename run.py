from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Zdravo, ovo je osnovna Flask aplikacija!"

if __name__ == '__main__':
    app.run(debug=True)
