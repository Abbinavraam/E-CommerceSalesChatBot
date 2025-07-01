#!/usr/bin/env python3
import sys
import traceback

try:
    print("Starting server test...")
    
    print("1. Importing modules...")
    from app import create_app, socketio, db
    print("   ✓ Modules imported successfully")
    
    print("2. Creating app...")
    app = create_app()
    print("   ✓ App created successfully")
    
    print("3. Testing app context...")
    with app.app_context():
        print("   ✓ App context working")
        
    print("4. Starting server...")
    print("   Server will be available at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
