from flask import Flask, render_template, url_for, request, Response

app = Flask(__name__)

@app.route('/login', methods=["POST","GET"])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)