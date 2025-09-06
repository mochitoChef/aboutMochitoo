#!/usr/bin/env python3
"""
Serve the portfolio website locally
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIRECTORY = "portfolio_clone"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    print("=" * 50)
    print("  PORTFOLIO WEBSITE SERVER")
    print("=" * 50)
    print(f"\n🚀 Starting server on port {PORT}...")
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"✅ Server running at: {url}")
        print(f"📁 Serving files from: {DIRECTORY}/")
        print("\n📋 Features:")
        print("  • Dark/Light theme toggle (sun icon)")
        print("  • Click email to copy")
        print("  • Interactive project cards")
        print("  • Smooth animations")
        print("\n⌨️  Press Ctrl+C to stop the server")
        
        # Open browser
        print(f"\n🌐 Opening browser...")
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()


