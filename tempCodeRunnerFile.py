@app.route("/load_application", methods=["GET", "POST"])
def application():
    return Content.load_application()