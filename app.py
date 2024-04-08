from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
<<<<<<< HEAD

=======
>>>>>>> 971d77e30fcdaf8951b730a780c33b46d59585da

if __name__ == '__main__':
    app.run(debug=True, port=8000)