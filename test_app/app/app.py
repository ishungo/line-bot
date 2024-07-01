from flask import Flask

# Flaskをappという変数で動かす宣言
app = Flask(__name__)

@app.route('/')
def hello():
   name = "Flask Hello World"
   return name

# appの実行
if __name__ == "__main__":
   app.run()
