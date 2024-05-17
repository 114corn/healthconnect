pip install Flask-Caching
```

```python
from flask_caching import Cache
from dotenv import load_dotenv
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from datetime import timedelta
import os

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)

app.config['CACHE_TYPE'] = 'SimpleCache' 
cache = Cache(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)

@app.route('/api/user/<username>', methods=['GET'])
@jwt_required()
def get_user(username):
    user_info = cache.get(username)
    if user_info is None:
        user = User.query.filter_by(username=username).first()
        if user:
            user_info = {'id': user.id, 'username': user.username}
            cache.set(username, user_info, timeout=5*60)  
        else:
            abort(404, description="User not found")
    return jsonify(user_info)

if __name__ == '__main__':
    app.run(debug=True)