#!/usr/bin/env python3
"""
Quick Start Script for Website Cloning
Run this to get started with cloning a website from screenshots
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed"""
    required = ['selenium', 'Pillow', 'beautifulsoup4', 'requests', 'numpy', 'scikit-learn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!")
    else:
        print("✅ All dependencies are installed!")


def main_menu():
    """Display main menu and handle user choice"""
    print("\n" + "=" * 60)
    print("🎨 WEBSITE CLONING FROM SCREENSHOTS - QUICK START")
    print("=" * 60)
    
    print("\nWhat would you like to do?")
    print("\n1. 📸 Capture screenshots from a website")
    print("2. 🔄 Convert existing screenshot to HTML/CSS")
    print("3. 🤖 Use AI to convert screenshot (requires API key)")
    print("4. 🚀 Full workflow: Capture + Convert")
    print("5. 📖 View documentation")
    print("6. ❌ Exit")
    
    choice = input("\nEnter your choice (1-6): ")
    return choice


def capture_screenshots():
    """Run screenshot capture"""
    print("\n📸 SCREENSHOT CAPTURE")
    print("-" * 40)
    
    try:
        from screenshot_capture import WebsiteScreenshotCapture
        
        url = input("Enter the website URL to capture: ")
        if not url.startswith("http"):
            url = "https://" + url
        
        print(f"\n🔍 Capturing screenshots from: {url}")
        capture = WebsiteScreenshotCapture(url)
        
        print("\n📸 Starting capture process...")
        capture.capture_full_page()
        capture.capture_viewport_sections()
        capture.extract_colors_and_fonts()
        capture.download_assets()
        
        print("\n✅ Screenshots captured successfully!")
        print(f"📁 Check the 'screenshots' folder for results")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during capture: {e}")
        print("Make sure you have ChromeDriver installed and in PATH")
        return False


def convert_screenshot():
    """Convert screenshot to HTML/CSS"""
    print("\n🔄 SCREENSHOT TO HTML/CSS CONVERSION")
    print("-" * 40)
    
    try:
        from screenshot_to_html import ScreenshotToHTML
        
        # List available screenshots
        screenshot_dir = Path("screenshots/full_page")
        if screenshot_dir.exists():
            screenshots = list(screenshot_dir.glob("*.png"))
            if screenshots:
                print("\n📸 Available screenshots:")
                for i, screenshot in enumerate(screenshots, 1):
                    print(f"{i}. {screenshot.name}")
                
                choice = input("\nEnter number or path to screenshot: ")
                
                if choice.isdigit() and 1 <= int(choice) <= len(screenshots):
                    screenshot_path = str(screenshots[int(choice) - 1])
                else:
                    screenshot_path = choice
            else:
                screenshot_path = input("Enter path to screenshot: ")
        else:
            screenshot_path = input("Enter path to screenshot: ")
        
        if not Path(screenshot_path).exists():
            print(f"❌ Screenshot not found: {screenshot_path}")
            return False
        
        print(f"\n🔄 Converting: {screenshot_path}")
        converter = ScreenshotToHTML(screenshot_path)
        result = converter.convert_to_html()
        
        print("\n✅ Conversion complete!")
        print(f"📁 HTML/CSS generated in 'cloned_site' folder")
        print(f"🎨 Extracted colors: {', '.join(result['colors'][:5])}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during conversion: {e}")
        return False


def ai_convert():
    """AI-powered screenshot conversion"""
    print("\n🤖 AI-POWERED CONVERSION")
    print("-" * 40)
    
    try:
        from ai_screenshot_converter import AIScreenshotConverter
        
        print("\nSelect AI service:")
        print("1. OpenAI GPT-4 Vision")
        print("2. Anthropic Claude")
        
        service_choice = input("\nEnter choice (1-2): ")
        service = "openai" if service_choice == "1" else "claude"
        
        # Check for API key
        env_key = f"{service.upper()}_API_KEY"
        if not os.getenv(env_key):
            print(f"\n⚠️  No {env_key} found in environment variables")
            api_key = input(f"Enter your {service} API key: ")
            if not api_key:
                print("❌ API key is required for AI conversion")
                return False
        else:
            api_key = None
            print(f"✅ Using {env_key} from environment")
        
        # Get screenshot
        screenshot_path = input("\nEnter path to screenshot: ")
        
        if not Path(screenshot_path).exists():
            print(f"❌ Screenshot not found: {screenshot_path}")
            return False
        
        instructions = input("Additional instructions (optional): ")
        
        print(f"\n🤖 Converting with {service}...")
        converter = AIScreenshotConverter(service, api_key)
        success = converter.convert_screenshot(screenshot_path, instructions)
        
        if success:
            print("\n✅ AI conversion complete!")
            print("📁 Check 'ai_generated' folder for results")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error during AI conversion: {e}")
        return False


def full_workflow():
    """Run complete workflow"""
    print("\n🚀 FULL WORKFLOW: CAPTURE + CONVERT")
    print("-" * 40)
    
    # Step 1: Capture
    if capture_screenshots():
        print("\n" + "=" * 40)
        print("Step 1 complete! Now let's convert...")
        print("=" * 40)
        
        # Step 2: Convert
        print("\nConversion method:")
        print("1. Basic HTML/CSS extraction")
        print("2. AI-powered conversion (requires API key)")
        
        method = input("\nEnter choice (1-2): ")
        
        if method == "2":
            ai_convert()
        else:
            convert_screenshot()
    
    print("\n🎉 Workflow complete!")


def view_docs():
    """Display quick documentation"""
    print("\n📖 QUICK DOCUMENTATION")
    print("=" * 60)
    
    print("""
🎯 PURPOSE:
This toolkit helps you clone websites from screenshots using various methods:
- Automated screenshot capture
- Color and layout extraction
- AI-powered HTML/CSS generation

📋 REQUIREMENTS:
- Python 3.8+
- Chrome browser + ChromeDriver
- Optional: OpenAI or Anthropic API key for AI conversion

🔧 BASIC WORKFLOW:
1. Capture screenshots of target website
2. Extract colors, fonts, and layout
3. Generate HTML/CSS code
4. Refine and customize

⚠️  LEGAL NOTE:
Only clone websites you own or have permission to clone.
Respect copyright and intellectual property rights.

📚 FILES:
- screenshot_capture.py: Capture website screenshots
- screenshot_to_html.py: Convert screenshots to HTML/CSS
- ai_screenshot_converter.py: AI-powered conversion
- README.md: Full documentation

💡 TIPS:
- Start with high-quality screenshots
- Use AI for complex layouts
- Always test responsive design
- Customize generated code to your needs
    """)
    
    input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    print("🔍 Checking dependencies...")
    check_dependencies()
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            capture_screenshots()
        elif choice == "2":
            convert_screenshot()
        elif choice == "3":
            ai_convert()
        elif choice == "4":
            full_workflow()
        elif choice == "5":
            view_docs()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        if choice != "6":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


