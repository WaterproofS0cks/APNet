@app.route("/load_applicant", methods=["GET", "POST"])
def applicant():
    return Content.load_applicants()
