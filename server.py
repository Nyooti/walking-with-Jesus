#!/usr/bin/env python3
"""
Simple HTTP Server for Walking with Jesus Christ Website
Run this script to serve the website on your local network
"""

import http.server
import socketserver
import webbrowser
import socket
import os
import sys

def get_local_ip():
    """Get the local IP address"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def start_server(port=8000):
    """Start the HTTP server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Get local IP
    local_ip = get_local_ip()
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("=" * 60)
            print("🌍 Walking with Jesus Christ Website Server")
            print("=" * 60)
            print(f"📁 Serving directory: {os.getcwd()}")
            print(f"🌐 Local access: http://localhost:{port}")
            print(f"🏠 Network access: http://{local_ip}:{port}")
            print(f"📱 Admin panel: http://{local_ip}:{port}/admin.html")
            print("=" * 60)
            print("📝 Other devices on your network can access using the Network URL")
            print("🔄 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open browser automatically
            try:
                webbrowser.open(f"http://localhost:{port}")
                print("🌐 Browser opened automatically")
            except:
                print("⚠️  Could not open browser automatically")
            
            print(f"\n🚀 Server started on port {port}...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python server.py --port {port + 1}")
            sys.exit(1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = 8000
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--port" and len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid port number")
                sys.exit(1)
        elif sys.argv[1] == "--help":
            print("Usage: python server.py [--port PORT]")
            print("Default port: 8000")
            print("Example: python server.py --port 8080")
            sys.exit(0)
    
    start_server(port)
