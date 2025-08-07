from flask import Flask, render_template
from compromised_ec2_response_simulator.routes.input import input_bp
from compromised_ec2_response_simulator.routes.actions import actions_bp

app = Flask(__name__)
app.secret_key = 'secret_key_here'

app.register_blueprint(input_bp)
app.register_blueprint(actions_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
