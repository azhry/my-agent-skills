"""
HTML-to-Image exporter for Data Science Lab infographics.
Converts custom, dynamically-generated HTML strings to high-res images using Playwright.
"""
import os
import base64

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def image_to_base64(image_path):
    """Utility helper to embed local plots into custom HTML."""
    if not os.path.exists(image_path):
        print(f"WARNING: Image not found at {image_path}")
        return ""
        
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            path_str = str(image_path)
            ext = path_str.split('.')[-1].lower()
            mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
            return f"data:{mime};base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return ""


def export_infographic(html_content, save_path, width=1920, height=1080):
    """Exports custom HTML string to a high-resolution PNG using Playwright."""
    os.makedirs(os.path.dirname(os.path.abspath(save_path)) or '.', exist_ok=True)
    
    if not PLAYWRIGHT_AVAILABLE:
        print("PLAYWRIGHT NOT INSTALLED. FALLING BACK TO HTML OUTPUT.")
        fallback_path = save_path.replace('.png', '.html').replace('.jpg', '.html')
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return fallback_path

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.set_content(html_content)
            
            # Wait for external fonts/charts to load
            page.wait_for_timeout(2000)
            
            # Optionally wait for rendering complete flag if the agent included it
            try:
                page.wait_for_function("window.__RENDERING_COMPLETE === true", timeout=3000)
            except:
                pass # Proceed if flag isn't found
                
            page.screenshot(path=save_path)
            browser.close()
            print(f"\n✅ Infographic successfully generated at: {save_path}")
            return save_path
    except Exception as e:
        print(f"EXPORT FAILED: {str(e)}")
        fallback_path = save_path.replace('.png', '.html').replace('.jpg', '.html')
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return fallback_path
