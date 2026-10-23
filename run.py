#from app import create_app

#app = create_app()

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)

#from app import create_app
#app = create_app()
#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000, debug=True)

from app import create_app, db
from flask import send_from_directory
import os

app = create_app()

with app.app_context():
    db.create_all()
    print("✓ users table checked/created")

@app.route('/app')
def serve_html():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'HVUntitled-2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)