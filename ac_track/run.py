from app import create_app, db
from flask_migrate import Migrate
import webbrowser

app = create_app()
migrate = Migrate(app, db)

from app.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/')

url = 'http://127.0.0.1:5000/login'

webbrowser.open_new_tab(url)



if __name__ == '__main__':
    app.run(debug=True)


