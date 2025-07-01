from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from app.models import ChatMessage, ChatSession, Product
from app import db, socketio
from datetime import datetime
import uuid
from . import bp

def process_message(message):
    """Process user message and generate appropriate response"""
    message_lower = message.lower()
    
    # Basic intent recognition
    if any(word in message_lower for word in ['hi', 'hello', 'hey']):
        return 'Hello! How can I help you with your shopping today?'
    
    elif any(word in message_lower for word in ['bye', 'goodbye', 'thank']):
        return 'Thank you for shopping with us! Have a great day!'
    
    elif 'product' in message_lower or 'search' in message_lower:
        # Extract potential search terms
        search_terms = [word for word in message_lower.split() 
                       if word not in ['product', 'search', 'for', 'find', 'me']]
        if search_terms:
            # Search for products
            search_query = '%' + '%'.join(search_terms) + '%'
            products = Product.query.filter(
                Product.name.ilike(search_query)
            ).limit(3).all()
            
            if products:
                response = "Here are some products that might interest you:\n"
                for product in products:
                    response += f"- {product.name}: ${product.price}\n"
                return response
            else:
                return "I couldn't find any products matching your request. Could you please try different keywords?"
    
    elif 'price' in message_lower:
        # Handle price-related queries
        return "Would you like to see our products in a specific price range? Please specify your budget."
    
    elif 'category' in message_lower:
        # Get available categories
        categories = db.session.query(Product.category).distinct().all()
        categories_list = [cat[0] for cat in categories if cat[0]]
        return f"We have products in the following categories: {', '.join(categories_list)}"
    
    # Default response
    return "I'm here to help you find the perfect product. You can ask me about specific products, categories, or prices!"

@bp.route('/start', methods=['POST'])
@jwt_required()
def start_session():
    user_id = get_jwt_identity()
    session_id = str(uuid.uuid4())
    
    # Create new chat session
    session = ChatSession(session_id=session_id, user_id=user_id)
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'session_id': session_id,
        'message': 'Chat session started'
    })

@bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['content', 'session_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Save user message
    user_message = ChatMessage(
        user_id=user_id,
        content=data['content'],
        session_id=data['session_id'],
        message_type='user'
    )
    db.session.add(user_message)
    
    # Process message and generate response
    bot_response = process_message(data['content'])
    
    # Save bot response
    bot_message = ChatMessage(
        user_id=user_id,
        content=bot_response,
        session_id=data['session_id'],
        message_type='bot'
    )
    db.session.add(bot_message)
    db.session.commit()
    
    # Emit messages via WebSocket
    socketio.emit('new_message', {
        'user_message': user_message.to_dict(),
        'bot_message': bot_message.to_dict()
    }, room=data['session_id'])
    
    return jsonify({
        'user_message': user_message.to_dict(),
        'bot_message': bot_message.to_dict()
    })

@bp.route('/history/<session_id>', methods=['GET'])
@jwt_required()
def get_chat_history(session_id):
    user_id = get_jwt_identity()
    
    messages = ChatMessage.query.filter_by(
        session_id=session_id,
        user_id=user_id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    return jsonify([message.to_dict() for message in messages])

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_user_sessions():
    user_id = get_jwt_identity()
    
    sessions = ChatSession.query.filter_by(
        user_id=user_id
    ).order_by(ChatSession.started_at.desc()).all()
    
    return jsonify([session.to_dict() for session in sessions])

@socketio.on('join')
def on_join(data):
    """Handle client joining a chat session"""
    room = data.get('session_id')
    if room:
        socketio.join_room(room)
        emit('status', {'message': f'Joined session {room}'}, room=room)

@socketio.on('leave')
def on_leave(data):
    """Handle client leaving a chat session"""
    room = data.get('session_id')
    if room:
        socketio.leave_room(room)
        emit('status', {'message': f'Left session {room}'}, room=room)