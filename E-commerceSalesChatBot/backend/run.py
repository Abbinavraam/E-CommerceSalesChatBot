from app import create_app, socketio, db
from app.models import User, Product, ChatMessage, ChatSession

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'ChatMessage': ChatMessage,
        'ChatSession': ChatSession
    }

if __name__ == '__main__':
    print("Starting Flask-SocketIO server...")
    print("Server will be available at: http://localhost:5000")
    # Run the application with WebSocket support
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)