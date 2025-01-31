# run.py
from flask import redirect, url_for
from app import create_app
import os

app = create_app()

# Root route
@app.route('/')
def index():
    return redirect(url_for('booking.index'))

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment variable or default to False
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    app.run(
        host='0.0.0.0',  # Makes the server externally visible
        port=port,
        debug=debug
    )