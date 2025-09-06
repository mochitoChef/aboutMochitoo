"""
Website Screenshot Capture Tool
Captures screenshots of websites for cloning purposes
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


class WebsiteScreenshotCapture:
    def __init__(self, url, output_dir="screenshots"):
        self.url = url
        self.output_dir = output_dir
        self.domain = urlparse(url).netloc
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/full_page", exist_ok=True)
        os.makedirs(f"{output_dir}/sections", exist_ok=True)
        os.makedirs(f"{output_dir}/mobile", exist_ok=True)
        
        # Setup Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        
    def capture_full_page(self, viewport_widths=[1920, 1366, 768, 375]):
        """Capture full page screenshots at different viewport widths"""
        driver = webdriver.Chrome(options=self.chrome_options)
        
        try:
            for width in viewport_widths:
                driver.set_window_size(width, 1080)
                driver.get(self.url)
                
                # Wait for page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(2)  # Extra wait for dynamic content
                
                # Get full page dimensions
                total_height = driver.execute_script("return document.body.scrollHeight")
                driver.set_window_size(width, total_height)
                
                # Take screenshot
                screenshot_path = f"{self.output_dir}/full_page/{self.domain}_w{width}.png"
                driver.save_screenshot(screenshot_path)
                print(f"Captured full page screenshot at {width}px width: {screenshot_path}")
                
        finally:
            driver.quit()
    
    def capture_viewport_sections(self, section_height=800):
        """Capture screenshots of viewport sections while scrolling"""
        driver = webdriver.Chrome(options=self.chrome_options)
        
        try:
            driver.set_window_size(1920, section_height)
            driver.get(self.url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            
            # Get page height
            total_height = driver.execute_script("return document.body.scrollHeight")
            
            # Scroll and capture sections
            scroll_position = 0
            section_num = 1
            
            while scroll_position < total_height:
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)  # Wait for scroll animation
                
                screenshot_path = f"{self.output_dir}/sections/{self.domain}_section_{section_num}.png"
                driver.save_screenshot(screenshot_path)
                print(f"Captured section {section_num}: {screenshot_path}")
                
                scroll_position += section_height - 100  # Overlap slightly
                section_num += 1
                
        finally:
            driver.quit()
    
    def capture_interactive_states(self):
        """Capture screenshots of interactive elements (hover states, dropdowns, etc.)"""
        driver = webdriver.Chrome(options=self.chrome_options)
        
        try:
            driver.set_window_size(1920, 1080)
            driver.get(self.url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            
            # Find interactive elements
            buttons = driver.find_elements(By.TAG_NAME, "button")
            links = driver.find_elements(By.TAG_NAME, "a")
            dropdowns = driver.find_elements(By.TAG_NAME, "select")
            
            # Capture hover states for buttons
            actions = ActionChains(driver)
            for i, button in enumerate(buttons[:5]):  # Limit to first 5 buttons
                try:
                    actions.move_to_element(button).perform()
                    time.sleep(0.5)
                    screenshot_path = f"{self.output_dir}/sections/button_hover_{i}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"Captured button hover state {i}")
                except:
                    pass
                    
        finally:
            driver.quit()
    
    def extract_colors_and_fonts(self):
        """Extract color palette and fonts from the website"""
        driver = webdriver.Chrome(options=self.chrome_options)
        
        try:
            driver.get(self.url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract colors
            colors = set()
            elements = driver.find_elements(By.CSS_SELECTOR, "*")
            
            for element in elements[:100]:  # Sample first 100 elements
                try:
                    bg_color = element.value_of_css_property("background-color")
                    text_color = element.value_of_css_property("color")
                    colors.add(bg_color)
                    colors.add(text_color)
                except:
                    pass
            
            # Extract fonts
            fonts = set()
            for element in elements[:100]:
                try:
                    font_family = element.value_of_css_property("font-family")
                    if font_family:
                        fonts.add(font_family)
                except:
                    pass
            
            # Save style information
            style_info = {
                "colors": list(colors),
                "fonts": list(fonts),
                "url": self.url
            }
            
            with open(f"{self.output_dir}/style_info.json", "w") as f:
                json.dump(style_info, f, indent=2)
            
            print(f"Extracted {len(colors)} colors and {len(fonts)} fonts")
            
        finally:
            driver.quit()
    
    def download_assets(self):
        """Download images and other assets from the website"""
        assets_dir = f"{self.output_dir}/assets"
        os.makedirs(assets_dir, exist_ok=True)
        
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Download images
            images = soup.find_all('img')
            for i, img in enumerate(images):
                try:
                    img_url = img.get('src')
                    if img_url:
                        if not img_url.startswith('http'):
                            img_url = urljoin(self.url, img_url)
                        
                        img_response = requests.get(img_url)
                        file_ext = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
                        
                        with open(f"{assets_dir}/image_{i}{file_ext}", "wb") as f:
                            f.write(img_response.content)
                        
                        print(f"Downloaded image {i}: {img_url}")
                except Exception as e:
                    print(f"Failed to download image: {e}")
                    
        except Exception as e:
            print(f"Failed to download assets: {e}")


def main():
    # Example usage
    url = input("Enter the website URL to clone: ")
    
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\nStarting screenshot capture for: {url}")
    print("-" * 50)
    
    capture = WebsiteScreenshotCapture(url)
    
    print("\n1. Capturing full page screenshots...")
    capture.capture_full_page()
    
    print("\n2. Capturing viewport sections...")
    capture.capture_viewport_sections()
    
    print("\n3. Capturing interactive states...")
    capture.capture_interactive_states()
    
    print("\n4. Extracting colors and fonts...")
    capture.extract_colors_and_fonts()
    
    print("\n5. Downloading assets...")
    capture.download_assets()
    
    print("\n✅ Screenshot capture complete!")
    print(f"Screenshots saved in: {capture.output_dir}/")


if __name__ == "__main__":
    main()
