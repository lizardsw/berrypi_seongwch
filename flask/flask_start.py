from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello():
	return "Hello Flask!\n"
@app.route('/bye')
def bye():
	return "byebye~"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port = "8080")
