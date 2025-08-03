import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from src.routes.cube import cube_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'
CORS(app)
app.register_blueprint(cube_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

