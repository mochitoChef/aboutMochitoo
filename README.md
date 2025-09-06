# Website Cloning from Screenshots 🖼️→💻

A comprehensive toolkit for cloning websites using screenshots. This project provides multiple approaches including automated screenshot capture, AI-powered conversion, and manual recreation tools.

## 🚀 Features

- **Automated Screenshot Capture**: Capture full-page screenshots, sections, and interactive states
- **AI-Powered Conversion**: Convert screenshots to HTML/CSS using GPT-4 Vision or Claude
- **Color & Style Extraction**: Automatically extract color palettes and fonts
- **Layout Detection**: Detect and recreate website sections
- **Asset Download**: Download images and resources from target websites
- **Responsive Design**: Generate mobile-friendly code

## 📋 Prerequisites

- Python 3.8+
- Chrome browser (for Selenium)
- ChromeDriver (download from https://chromedriver.chromium.org/)

## 🔧 Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd aboutme
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download ChromeDriver and add to PATH or place in project directory

## 📖 Usage Guide

### Method 1: Complete Website Cloning (Recommended)

This method captures screenshots and converts them to code:

```bash
python screenshot_capture.py
```

Enter the website URL when prompted. The script will:
1. Capture full-page screenshots at multiple viewport widths
2. Capture scrolling sections
3. Extract colors and fonts
4. Download assets

Then convert screenshots to HTML:

```bash
python screenshot_to_html.py
```

### Method 2: AI-Powered Conversion

For the most accurate results, use AI to convert screenshots:

```bash
python ai_screenshot_converter.py
```

You'll need an API key from either:
- **OpenAI**: Sign up at https://platform.openai.com/
- **Anthropic**: Sign up at https://www.anthropic.com/

Set your API key as an environment variable:
```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

### Method 3: Manual Screenshot Conversion

If you already have screenshots:

```bash
python screenshot_to_html.py
```

This will:
- Extract dominant colors
- Detect layout sections
- Generate HTML/CSS template
- Create responsive design

## 🛠️ Tools Overview

### `screenshot_capture.py`
Captures comprehensive screenshots of any website:
- Full-page captures at different viewport widths (desktop, tablet, mobile)
- Section-by-section captures while scrolling
- Interactive state captures (hover effects, dropdowns)
- Asset downloading (images, icons)
- Style extraction (colors, fonts)

### `screenshot_to_html.py`
Converts screenshots to HTML/CSS code:
- Color palette extraction using K-means clustering
- Layout section detection
- Responsive HTML structure generation
- Modern CSS with CSS variables
- Mobile-first responsive design

### `ai_screenshot_converter.py`
Uses AI models for accurate conversion:
- Supports OpenAI GPT-4 Vision
- Supports Anthropic Claude
- Batch conversion for multiple screenshots
- Generates semantic HTML5
- Creates modern, accessible code

## 📁 Output Structure

After running the tools, you'll get:

```
screenshots/
├── full_page/         # Full page captures
├── sections/          # Sectioned captures
├── mobile/           # Mobile viewport captures
├── assets/           # Downloaded images
└── style_info.json  # Extracted styles

cloned_site/
├── index.html        # Generated HTML
├── styles.css        # Generated CSS
└── script.js         # Generated JavaScript

ai_generated/
├── index.html        # AI-generated HTML
├── styles.css        # AI-generated CSS
├── script.js         # AI-generated JavaScript
└── ai_response.txt   # Full AI response
```

## 🎯 Best Practices

### For Screenshot Capture:
1. Ensure the website is fully loaded before capturing
2. Capture at multiple viewport widths for responsive design
3. Include interactive states (hover, active, focus)
4. Save style information for accurate recreation

### For AI Conversion:
1. Use high-quality, complete screenshots
2. Provide clear instructions to the AI
3. Review and refine generated code
4. Test responsiveness across devices

### For Manual Conversion:
1. Start with the extracted color palette
2. Focus on layout structure first
3. Add content progressively
4. Test frequently in browser

## 🔍 Advanced Features

### Batch Processing
Convert multiple screenshots at once:
```python
from ai_screenshot_converter import AIScreenshotConverter

converter = AIScreenshotConverter(service="openai")
converter.batch_convert("screenshots/full_page/", "output/")
```

### Custom Styling
Modify extracted colors in `style_info.json` before conversion:
```json
{
  "colors": ["#007bff", "#6c757d", "#333333", "#ffffff"],
  "fonts": ["Helvetica Neue", "Arial", "sans-serif"]
}
```

### Section Detection
Adjust section detection sensitivity:
```python
converter = ScreenshotToHTML("screenshot.png")
sections = converter.detect_layout_sections(threshold=230)  # Adjust threshold
```

## 🤝 Workflow Tips

### Recommended Workflow:

1. **Capture**: Use `screenshot_capture.py` to get comprehensive screenshots
2. **AI Convert**: Use `ai_screenshot_converter.py` for initial code generation
3. **Refine**: Use `screenshot_to_html.py` for style extraction and refinement
4. **Customize**: Manually adjust the generated code to match exactly

### For Complex Websites:

1. Break down into components (header, sections, footer)
2. Convert each component separately
3. Combine and refine the complete page
4. Add interactions and animations

## ⚠️ Legal Considerations

**Important**: Always respect copyright and intellectual property rights:
- Only clone websites you own or have permission to clone
- This tool is for learning and development purposes
- Check website terms of service before cloning
- Give credit where appropriate
- Don't use cloned sites for impersonation or fraud

## 🐛 Troubleshooting

### ChromeDriver Issues:
- Ensure ChromeDriver version matches Chrome browser version
- Add ChromeDriver to system PATH or specify path in code

### API Key Issues:
- Check API key is valid and has sufficient credits
- Ensure environment variables are set correctly
- Use `.env` file for managing API keys

### Screenshot Quality:
- Increase wait times for dynamic content
- Disable ad blockers that might interfere
- Use headless=False for debugging

## 📚 Additional Resources

### Free Alternatives:
- **Screenshot to Code** (online): screenshot-to-code.com
- **HTML/CSS Extractor** extensions for Chrome/Firefox
- **Figma to HTML** plugins

### Manual Tools:
- Chrome DevTools for inspecting elements
- ColorZilla for color picking
- WhatFont for font identification
- Responsive Design Mode for testing

## 🎨 Example Use Cases

1. **Learning Web Development**: Study how professional websites are built
2. **Rapid Prototyping**: Quickly create mockups based on existing designs
3. **Design Inspiration**: Extract color schemes and layouts
4. **Migration Projects**: Convert old websites to modern standards
5. **Competitive Analysis**: Understand competitor design choices

## 📈 Performance Tips

- Use smaller screenshots for faster AI processing
- Cache API responses to avoid repeated calls
- Process screenshots in parallel for batch operations
- Optimize images before including in final site

## 🔮 Future Enhancements

- [ ] Support for more AI models (Gemini, local LLMs)
- [ ] Animation and interaction detection
- [ ] Component library generation
- [ ] Figma/Sketch export
- [ ] Real-time preview
- [ ] Version control integration

## 💡 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share your cloned sites

## 📄 License

This project is for educational purposes. Please respect website copyrights and terms of service.

---

**Note**: This tool is meant for learning and legitimate development purposes only. Always ensure you have the right to clone and use website designs.
