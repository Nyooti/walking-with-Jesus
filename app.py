#!/usr/bin/env python3
"""
Flask Backend for Walking with Jesus Christ Website
Handles blog CRUD operations and other API endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data storage file
BLOGS_FILE = 'blogs.json'

def load_blogs():
    """Load blogs from JSON file"""
    if os.path.exists(BLOGS_FILE):
        try:
            with open(BLOGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_blogs(blogs):
    """Save blogs to JSON file"""
    with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, ensure_ascii=False, indent=2)

# Blog API Routes
@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    """Get all blog posts"""
    try:
        blogs = load_blogs()
        # Sort by date (newest first)
        blogs.sort(key=lambda x: x.get('date', ''), reverse=True)
        return jsonify({'success': True, 'data': blogs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blogs/<blog_id>', methods=['GET'])
def get_blog(blog_id):
    """Get a specific blog post"""
    try:
        blogs = load_blogs()
        blog = next((b for b in blogs if str(b.get('id')) == str(blog_id)), None)
        if blog:
            return jsonify({'success': True, 'data': blog})
        else:
            return jsonify({'success': False, 'error': 'Blog not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blogs', methods=['POST'])
def create_blog():
    """Create a new blog post"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('content'):
            return jsonify({'success': False, 'error': 'Title and content are required'}), 400
        
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
        blogs = load_blogs()
        blogs.insert(0, new_blog)  # Add to beginning
        save_blogs(blogs)
        
        return jsonify({'success': True, 'data': new_blog}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blogs/<blog_id>', methods=['PUT'])
def update_blog(blog_id):
    """Update an existing blog post"""
    try:
        data = request.get_json()
        blogs = load_blogs()
        
        # Find the blog to update
        blog_index = next((i for i, b in enumerate(blogs) if str(b.get('id')) == str(blog_id)), None)
        
        if blog_index is None:
            return jsonify({'success': False, 'error': 'Blog not found'}), 404
        
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
        
        save_blogs(blogs)
        return jsonify({'success': True, 'data': blog})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blogs/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    """Delete a blog post"""
    try:
        blogs = load_blogs()
        
        # Find and remove the blog
        blog_index = next((i for i, b in enumerate(blogs) if str(b.get('id')) == str(blog_id)), None)
        
        if blog_index is None:
            return jsonify({'success': False, 'error': 'Blog not found'}), 404
        
        deleted_blog = blogs.pop(blog_index)
        save_blogs(blogs)
        
        return jsonify({'success': True, 'data': deleted_blog})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Static file serving
@app.route('/')
def serve_index():
    """Serve the main index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/admin.html')
def serve_admin():
    """Serve the admin.html"""
    return send_from_directory('.', 'admin.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🌍 Walking with Jesus Christ Website Backend")
    print("=" * 50)
    print("🚀 Starting Flask server...")
    print("📝 Blog API endpoints:")
    print("   GET    /api/blogs           - Get all blogs")
    print("   GET    /api/blogs/<id>      - Get specific blog")
    print("   POST   /api/blogs           - Create new blog")
    print("   PUT    /api/blogs/<id>      - Update blog")
    print("   DELETE /api/blogs/<id>      - Delete blog")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
