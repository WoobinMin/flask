from flask import Flask, render_template
import HTMLConverter as converter


app = Flask(__name__)
 
@app.route("/")
def main():
    converter.ConvertToHTML()
    return render_template('VisualHTML.html')
 
if __name__ == '__main__':
    app.run()