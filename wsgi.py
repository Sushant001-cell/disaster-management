"""
WSGI entry point for production deployment with Gunicorn
"""
from backend.app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
