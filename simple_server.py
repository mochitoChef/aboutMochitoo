#!/usr/bin/env python3
"""
Simple HTTP Server for Portfolio
Uses a different approach with basic HTTP server
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
import time

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="portfolio_clone", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"📄 {self.address_string()} - {format % args}")

def start_server():
    PORT = 8080
    DIRECTORY = "portfolio_clone"
    
    # Change to the directory containing the portfolio
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not os.path.exists(DIRECTORY):
        print(f"❌ Error: {DIRECTORY} directory not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Contents: {os.listdir('.')}")
        return
    
    print("=" * 60)
    print("  🚀 SIMPLE PORTFOLIO SERVER")
    print("=" * 60)
    print(f"\n📁 Serving from: {os.path.abspath(DIRECTORY)}")
    print(f"🌐 URL: http://localhost:{PORT}")
    print(f"📋 Files in directory:")
    
    for file in os.listdir(DIRECTORY):
        file_path = os.path.join(DIRECTORY, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            print(f"   • {file} ({size:,} bytes)")
    
    print(f"\n✅ Server starting on port {PORT}...")
    
    try:
        with HTTPServer(("", PORT), CustomHandler) as httpd:
            print(f"🎉 Server running at: http://localhost:{PORT}")
            print("⌨️  Press Ctrl+C to stop")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{PORT}")
                print("🌐 Browser opened!")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Port {PORT} is already in use. Trying port {PORT + 1}...")
            start_server_port(PORT + 1)
        else:
            print(f"❌ Error starting server: {e}")

def start_server_port(port):
    try:
        with HTTPServer(("", port), CustomHandler) as httpd:
            print(f"🎉 Server running at: http://localhost:{port}")
            print("⌨️  Press Ctrl+C to stop")
            webbrowser.open(f"http://localhost:{port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server()
