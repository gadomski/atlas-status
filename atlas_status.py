from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def atlas_status():
    return render_template("atlas_status.html")

if __name__ == "__main__":
    app.run(debug=True)
