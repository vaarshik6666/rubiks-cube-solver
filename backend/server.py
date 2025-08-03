from flask import Flask, render_template
from cube import cube_bp

app = Flask(__name__)
app.register_blueprint(cube_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)