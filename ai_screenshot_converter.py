"""
AI-Powered Screenshot to Code Converter
Uses AI models to convert screenshots into HTML/CSS/JavaScript code
"""

import os
import base64
import json
from typing import Dict, List, Optional
import requests
from PIL import Image
import io


class AIScreenshotConverter:
    """Convert screenshots to code using various AI services"""
    
    def __init__(self, service="openai", api_key=None):
        self.service = service
        self.api_key = api_key or os.getenv(f"{service.upper()}_API_KEY")
        
        if not self.api_key:
            print(f"Warning: No API key found for {service}. Set {service.upper()}_API_KEY environment variable.")
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def convert_with_openai(self, image_path: str, instructions: str = "") -> Dict:
        """Use OpenAI's GPT-4 Vision to convert screenshot to code"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}
        
        base64_image = self.encode_image(image_path)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert web developer. Convert the provided screenshot into clean, 
                    semantic HTML/CSS code. Focus on:
                    1. Proper HTML5 structure
                    2. Responsive CSS with flexbox/grid
                    3. Clean, maintainable code
                    4. Accessibility best practices
                    5. Modern CSS techniques"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Convert this screenshot to HTML/CSS code. {instructions}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result['choices'][0]['message']['content']
                return self.parse_code_response(code)
            else:
                return {"error": f"API error: {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    def convert_with_claude(self, image_path: str, instructions: str = "") -> Dict:
        """Use Anthropic's Claude to convert screenshot to code"""
        if not self.api_key:
            return {"error": "Anthropic API key not configured"}
        
        base64_image = self.encode_image(image_path)
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Convert this screenshot into HTML/CSS code. 
                            Requirements:
                            - Clean, semantic HTML5
                            - Modern CSS with variables
                            - Responsive design
                            - Proper structure and formatting
                            {instructions}"""
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result['content'][0]['text']
                return self.parse_code_response(code)
            else:
                return {"error": f"API error: {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    def parse_code_response(self, response: str) -> Dict:
        """Parse AI response to extract HTML, CSS, and JS code"""
        result = {
            "html": "",
            "css": "",
            "javascript": "",
            "full_response": response
        }
        
        # Extract HTML
        if "```html" in response:
            html_start = response.find("```html") + 7
            html_end = response.find("```", html_start)
            result["html"] = response[html_start:html_end].strip()
        elif "<html" in response.lower():
            html_start = response.lower().find("<!doctype html") if "<!doctype html" in response.lower() else response.lower().find("<html")
            html_end = response.lower().find("</html>") + 7
            if html_start != -1 and html_end > html_start:
                result["html"] = response[html_start:html_end]
        
        # Extract CSS
        if "```css" in response:
            css_start = response.find("```css") + 6
            css_end = response.find("```", css_start)
            result["css"] = response[css_start:css_end].strip()
        elif "<style>" in response:
            style_start = response.find("<style>") + 7
            style_end = response.find("</style>")
            if style_start != -1 and style_end > style_start:
                result["css"] = response[style_start:style_end].strip()
        
        # Extract JavaScript
        if "```javascript" in response or "```js" in response:
            js_marker = "```javascript" if "```javascript" in response else "```js"
            js_start = response.find(js_marker) + len(js_marker)
            js_end = response.find("```", js_start)
            result["javascript"] = response[js_start:js_end].strip()
        elif "<script>" in response:
            script_start = response.find("<script>") + 8
            script_end = response.find("</script>")
            if script_start != -1 and script_end > script_start:
                result["javascript"] = response[script_start:script_end].strip()
        
        return result
    
    def convert_screenshot(self, image_path: str, instructions: str = "", output_dir: str = "ai_generated") -> bool:
        """Main method to convert screenshot to code"""
        print(f"Converting screenshot using {self.service}...")
        
        if self.service == "openai":
            result = self.convert_with_openai(image_path, instructions)
        elif self.service == "claude":
            result = self.convert_with_claude(image_path, instructions)
        else:
            print(f"Unsupported service: {self.service}")
            return False
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if "details" in result:
                print(f"Details: {result['details']}")
            return False
        
        # Save generated code
        os.makedirs(output_dir, exist_ok=True)
        
        if result["html"]:
            with open(f"{output_dir}/index.html", "w", encoding='utf-8') as f:
                f.write(result["html"])
            print(f"✅ HTML saved to {output_dir}/index.html")
        
        if result["css"]:
            with open(f"{output_dir}/styles.css", "w", encoding='utf-8') as f:
                f.write(result["css"])
            print(f"✅ CSS saved to {output_dir}/styles.css")
        
        if result["javascript"]:
            with open(f"{output_dir}/script.js", "w", encoding='utf-8') as f:
                f.write(result["javascript"])
            print(f"✅ JavaScript saved to {output_dir}/script.js")
        
        # Save full response for reference
        with open(f"{output_dir}/ai_response.txt", "w", encoding='utf-8') as f:
            f.write(result["full_response"])
        
        return True
    
    def batch_convert(self, screenshot_dir: str, output_base_dir: str = "ai_generated"):
        """Convert multiple screenshots"""
        screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for i, screenshot in enumerate(screenshots):
            print(f"\nProcessing {i+1}/{len(screenshots)}: {screenshot}")
            image_path = os.path.join(screenshot_dir, screenshot)
            output_dir = os.path.join(output_base_dir, f"page_{i+1}")
            
            self.convert_screenshot(image_path, output_dir=output_dir)


class ScreenshotEnhancer:
    """Enhance screenshots for better AI conversion"""
    
    @staticmethod
    def add_annotations(image_path: str, output_path: str = None):
        """Add annotations to help AI understand the layout"""
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Add grid overlay to help AI understand sections
        width, height = img.size
        grid_size = 100
        
        # Draw subtle grid
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 0, 30), width=1)
        
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 0, 0, 30), width=1)
        
        # Save annotated image
        if output_path:
            img.save(output_path)
        else:
            base, ext = os.path.splitext(image_path)
            img.save(f"{base}_annotated{ext}")
        
        return img


def interactive_converter():
    """Interactive command-line interface for conversion"""
    print("=" * 60)
    print("AI-POWERED SCREENSHOT TO CODE CONVERTER")
    print("=" * 60)
    
    print("\nSelect AI Service:")
    print("1. OpenAI GPT-4 Vision")
    print("2. Anthropic Claude")
    print("3. Local Processing (Basic)")
    
    choice = input("\nEnter choice (1-3): ")
    
    service_map = {
        "1": "openai",
        "2": "claude",
        "3": "local"
    }
    
    service = service_map.get(choice, "openai")
    
    if service in ["openai", "claude"]:
        api_key = input(f"Enter {service.upper()} API key (or press Enter to use env variable): ")
        if api_key:
            converter = AIScreenshotConverter(service, api_key)
        else:
            converter = AIScreenshotConverter(service)
    else:
        # Use local converter
        from screenshot_to_html import ScreenshotToHTML
        screenshot_path = input("Enter screenshot path: ")
        converter = ScreenshotToHTML(screenshot_path)
        converter.convert_to_html()
        return
    
    print("\nConversion Options:")
    print("1. Single screenshot")
    print("2. Batch conversion (folder)")
    
    mode = input("\nEnter choice (1-2): ")
    
    if mode == "1":
        screenshot_path = input("Enter screenshot path: ")
        instructions = input("Additional instructions (optional): ")
        converter.convert_screenshot(screenshot_path, instructions)
    else:
        screenshot_dir = input("Enter screenshot directory: ")
        converter.batch_convert(screenshot_dir)
    
    print("\n✅ Conversion complete!")


if __name__ == "__main__":
    interactive_converter()
