#!/usr/bin/env python3
"""
Simple Backend for Walking with Jesus Christ Website
Handles blog CRUD operations using built-in HTTP server
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime
import uuid

# Data storage file
BLOGS_FILE = 'blogs.json'

class BlogAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/api/blogs'):
            self.handle_get_blogs()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/blogs':
            self.handle_create_blog()
        else:
            self.send_error(404)
    
    def do_PUT(self):
        """Handle PUT requests"""
        if self.path.startswith('/api/blogs/'):
            blog_id = self.path.split('/')[-1]
            self.handle_update_blog(blog_id)
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if self.path.startswith('/api/blogs/'):
            blog_id = self.path.split('/')[-1]
            self.handle_delete_blog(blog_id)
        else:
            self.send_error(404)
    
    def load_blogs(self):
        """Load blogs from JSON file"""
        if os.path.exists(BLOGS_FILE):
            try:
                with open(BLOGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_blogs(self, blogs):
        """Save blogs to JSON file"""
        with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(blogs, f, ensure_ascii=False, indent=2)
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def handle_get_blogs(self):
        """Handle GET /api/blogs requests"""
        try:
            blogs = self.load_blogs()
            # Sort by date (newest first)
            blogs.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            if len(self.path.split('/')) > 3:  # Get specific blog
                blog_id = self.path.split('/')[-1]
                blog = next((b for b in blogs if str(b.get('id')) == str(blog_id)), None)
                if blog:
                    self.send_json_response({'success': True, 'data': blog})
                else:
                    self.send_json_response({'success': False, 'error': 'Blog not found'}, 404)
            else:  # Get all blogs
                self.send_json_response({'success': True, 'data': blogs})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_create_blog(self):
        """Handle POST /api/blogs requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            if not data.get('title') or not data.get('content'):
                self.send_json_response({'success': False, 'error': 'Title and content are required'}, 400)
                return
            
            # Create new blog
            new_blog = {
                'id': str(uuid.uuid4()),
                'title': data.get('title', '').strip(),
                'author': data.get('author', 'Habert Oyolla').strip(),
                'category': data.get('category', 'Christian Theology'),
                'content': data.get('content', '').strip(),
                'image': data.get('image', '').strip(),
                'tags': [tag.strip() for tag in data.get('tags', '').split(',') if tag.strip()] if data.get('tags') else [],
                'date': datetime.now().strftime('%B %d, %Y'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Calculate read time
            word_count = len(new_blog['content'].split())
            new_blog['readTime'] = f"{max(1, round(word_count / 200))} min read"
            
            # Load existing blogs and add new one
            blogs = self.load_blogs()
            blogs.insert(0, new_blog)  # Add to beginning
            self.save_blogs(blogs)
            
            self.send_json_response({'success': True, 'data': new_blog}, 201)
            
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_update_blog(self, blog_id):
        """Handle PUT /api/blogs/<id> requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            blogs = self.load_blogs()
            
            # Find the blog to update
            blog_index = next((i for i, b in enumerate(blogs) if str(b.get('id')) == str(blog_id)), None)
            
            if blog_index is None:
                self.send_json_response({'success': False, 'error': 'Blog not found'}, 404)
                return
            
            # Update blog fields
            blog = blogs[blog_index]
            blog.update({
                'title': data.get('title', blog['title']).strip(),
                'author': data.get('author', blog['author']).strip(),
                'category': data.get('category', blog['category']),
                'content': data.get('content', blog['content']).strip(),
                'image': data.get('image', blog['image']).strip(),
                'tags': [tag.strip() for tag in data.get('tags', '').split(',') if tag.strip()] if data.get('tags') else blog['tags'],
                'updated_at': datetime.now().isoformat()
            })
            
            # Recalculate read time
            word_count = len(blog['content'].split())
            blog['readTime'] = f"{max(1, round(word_count / 200))} min read"
            
            self.save_blogs(blogs)
            self.send_json_response({'success': True, 'data': blog})
            
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_delete_blog(self, blog_id):
        """Handle DELETE /api/blogs/<id> requests"""
        try:
            blogs = self.load_blogs()
            
            # Find and remove the blog
            blog_index = next((i for i, b in enumerate(blogs) if str(b.get('id')) == str(blog_id)), None)
            
            if blog_index is None:
                self.send_json_response({'success': False, 'error': 'Blog not found'}, 404)
                return
            
            deleted_blog = blogs.pop(blog_index)
            self.save_blogs(blogs)
            
            self.send_json_response({'success': True, 'data': deleted_blog})
            
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)

def start_backend(port=5000):
    """Start the backend server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        with socketserver.TCPServer(("", port), BlogAPIHandler) as httpd:
            print("=" * 60)
            print("🌍 Walking with Jesus Christ Website Backend")
            print("=" * 60)
            print(f"📁 Serving directory: {os.getcwd()}")
            print(f"🚀 Backend server running on port {port}")
            print(f"🌐 API endpoints: http://localhost:{port}/api/blogs")
            print("=" * 60)
            print("📝 Available API endpoints:")
            print("   GET    /api/blogs           - Get all blogs")
            print("   GET    /api/blogs/<id>      - Get specific blog")
            print("   POST   /api/blogs           - Create new blog")
            print("   PUT    /api/blogs/<id>      - Update blog")
            print("   DELETE /api/blogs/<id>      - Delete blog")
            print("=" * 60)
            print("🔄 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python3 backend.py --port {port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    import sys
    port = 5000
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--port" and len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid port number")
                sys.exit(1)
        elif sys.argv[1] == "--help":
            print("Usage: python3 backend.py [--port PORT]")
            print("Default port: 5000")
            print("Example: python3 backend.py --port 8080")
            sys.exit(0)
    
    start_backend(port)
