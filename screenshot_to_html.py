"""
Screenshot to HTML Converter
Helps convert website screenshots into HTML/CSS code
"""

import os
import base64
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys


class ScreenshotToHTML:
    def __init__(self, screenshot_path):
        self.screenshot_path = screenshot_path
        self.image = Image.open(screenshot_path)
        self.width, self.height = self.image.size
        
    def extract_color_palette(self, n_colors=10):
        """Extract dominant colors from screenshot"""
        # Resize image for faster processing
        img_small = self.image.resize((150, 150))
        img_array = np.array(img_small)
        
        # Reshape image to be a list of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Use KMeans to find dominant colors
        kmeans = KMeans(n_clusters=n_colors, random_state=42)
        kmeans.fit(pixels)
        
        # Get colors
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert to hex
        hex_colors = []
        for color in colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            hex_colors.append(hex_color)
        
        return hex_colors
    
    def detect_layout_sections(self):
        """Detect major layout sections in the screenshot"""
        # Convert to grayscale for edge detection
        img_gray = self.image.convert('L')
        img_array = np.array(img_gray)
        
        # Simple section detection based on horizontal lines
        sections = []
        threshold = 240  # Light colors often indicate section boundaries
        
        # Find rows that are mostly light (potential section boundaries)
        row_means = np.mean(img_array, axis=1)
        boundaries = []
        
        for i in range(1, len(row_means)-1):
            if row_means[i] > threshold and row_means[i-1] <= threshold:
                boundaries.append(i)
        
        # Create sections from boundaries
        if not boundaries:
            boundaries = [0, self.height // 3, 2 * self.height // 3, self.height]
        
        for i in range(len(boundaries) - 1):
            sections.append({
                'top': boundaries[i],
                'bottom': boundaries[i+1],
                'height': boundaries[i+1] - boundaries[i]
            })
        
        return sections
    
    def generate_html_structure(self, sections, colors):
        """Generate HTML structure based on detected sections"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloned Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header Section -->
    <header class="site-header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-brand">
                    <a href="#" class="logo">Your Logo</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
                <div class="nav-toggle" id="navToggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main>
"""
        
        # Add sections based on detection
        for i, section in enumerate(sections):
            section_class = self._guess_section_type(i, len(sections))
            html += f"""
        <!-- Section {i+1} -->
        <section class="{section_class}" data-height="{section['height']}">
            <div class="container">
                <div class="section-content">
                    <h2>Section {i+1} Title</h2>
                    <p>Replace this with your content based on the screenshot.</p>
                    <!-- Add more content as needed -->
                </div>
            </div>
        </section>
"""
        
        html += """
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>About</h3>
                    <p>Footer content here</p>
                </div>
                <div class="footer-section">
                    <h3>Links</h3>
                    <ul>
                        <li><a href="#">Link 1</a></li>
                        <li><a href="#">Link 2</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact</h3>
                    <p>Contact information</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Your Website. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""
        
        return html
    
    def generate_css_styles(self, colors):
        """Generate CSS based on extracted colors"""
        primary_color = colors[0] if colors else "#007bff"
        secondary_color = colors[1] if len(colors) > 1 else "#6c757d"
        text_color = colors[2] if len(colors) > 2 else "#333333"
        bg_color = colors[3] if len(colors) > 3 else "#ffffff"
        
        css = f"""/* CSS Variables for Color Scheme */
:root {{
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --text-color: {text_color};
    --bg-color: {bg_color};
    --light-gray: #f8f9fa;
    --border-color: #dee2e6;
}}

/* Reset and Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: var(--text-color);
    background-color: var(--bg-color);
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Header Styles */
.site-header {{
    background-color: var(--bg-color);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}}

.navbar {{
    padding: 1rem 0;
}}

.navbar .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.nav-brand .logo {{
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}}

.nav-menu {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav-menu a {{
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.3s;
}}

.nav-menu a:hover {{
    color: var(--primary-color);
}}

.nav-toggle {{
    display: none;
    flex-direction: column;
    cursor: pointer;
}}

.nav-toggle span {{
    width: 25px;
    height: 3px;
    background-color: var(--text-color);
    margin: 3px 0;
    transition: 0.3s;
}}

/* Section Styles */
.hero-section {{
    padding: 4rem 0;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    text-align: center;
}}

.content-section {{
    padding: 3rem 0;
    background-color: var(--bg-color);
}}

.feature-section {{
    padding: 3rem 0;
    background-color: var(--light-gray);
}}

.section-content {{
    padding: 2rem 0;
}}

.section-content h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
}}

.section-content p {{
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1rem;
}}

/* Grid Layouts */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.card {{
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}}

/* Footer Styles */
.site-footer {{
    background-color: #2c3e50;
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 3rem;
}}

.footer-content {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}}

.footer-section h3 {{
    margin-bottom: 1rem;
    color: white;
}}

.footer-section ul {{
    list-style: none;
}}

.footer-section a {{
    color: #ecf0f1;
    text-decoration: none;
    transition: color 0.3s;
}}

.footer-section a:hover {{
    color: var(--primary-color);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #34495e;
    color: #95a5a6;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .nav-menu {{
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background-color: var(--bg-color);
        flex-direction: column;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .nav-menu.active {{
        display: flex;
    }}
    
    .nav-toggle {{
        display: flex;
    }}
    
    .grid {{
        grid-template-columns: 1fr;
    }}
    
    .footer-content {{
        grid-template-columns: 1fr;
    }}
}}

/* Utility Classes */
.text-center {{
    text-align: center;
}}

.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s, transform 0.3s;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}}

.btn:hover {{
    background-color: var(--secondary-color);
    transform: translateY(-2px);
}}

.btn-secondary {{
    background-color: var(--secondary-color);
}}

.btn-outline {{
    background-color: transparent;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}}

.btn-outline:hover {{
    background-color: var(--primary-color);
    color: white;
}}

/* Additional extracted colors as accent options */
/* Color Palette: {', '.join(colors)} */
"""
        
        return css
    
    def _guess_section_type(self, index, total_sections):
        """Guess section type based on position"""
        if index == 0:
            return "hero-section"
        elif index == total_sections - 1:
            return "cta-section"
        elif index % 2 == 0:
            return "feature-section"
        else:
            return "content-section"
    
    def convert_to_html(self, output_dir="cloned_site"):
        """Main conversion method"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("Extracting color palette...")
        colors = self.extract_color_palette()
        
        print("Detecting layout sections...")
        sections = self.detect_layout_sections()
        
        print("Generating HTML structure...")
        html = self.generate_html_structure(sections, colors)
        
        print("Generating CSS styles...")
        css = self.generate_css_styles(colors)
        
        # Save files
        with open(f"{output_dir}/index.html", "w") as f:
            f.write(html)
        
        with open(f"{output_dir}/styles.css", "w") as f:
            f.write(css)
        
        # Generate JavaScript
        js = """// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add any additional JavaScript functionality here
});"""
        
        with open(f"{output_dir}/script.js", "w") as f:
            f.write(js)
        
        print(f"\n✅ HTML/CSS/JS generated in {output_dir}/")
        print(f"Extracted colors: {colors}")
        print(f"Detected {len(sections)} sections")
        
        return {
            'colors': colors,
            'sections': sections,
            'output_dir': output_dir
        }


def main():
    screenshot_path = input("Enter path to screenshot: ")
    
    if os.path.exists(screenshot_path):
        converter = ScreenshotToHTML(screenshot_path)
        result = converter.convert_to_html()
        
        print("\n📝 Next steps:")
        print("1. Open index.html in your browser")
        print("2. Compare with the screenshot")
        print("3. Adjust the HTML content and CSS styles")
        print("4. Add actual content from the screenshot")
    else:
        print(f"Screenshot not found: {screenshot_path}")


if __name__ == "__main__":
    main()
