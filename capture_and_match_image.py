import os
import cv2
import numpy as np
from playwright.sync_api import sync_playwright
import matplotlib.pyplot as plt

# Function to check if image template is present in screenshot and display visually
def find_and_display_image_in_screenshot(screenshot_path, image_path):
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if screenshot is None:
        print(f"Error: Unable to read screenshot from {screenshot_path}")
        return

    if image is None:
        print(f"Error: Unable to read image template from {image_path}")
        return

    # Perform template matching
    result = cv2.matchTemplate(screenshot_rgb, image_rgb, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust threshold as needed

    # Get coordinates of matched area
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        bottom_right = (pt[0] + image_rgb.shape[1], pt[1] + image_rgb.shape[0])
        cv2.rectangle(screenshot_rgb, pt, bottom_right, (0, 255, 0), 2)

    # Display result using matplotlib
    plt.figure(figsize=(10, 6))
    plt.subplot(121)
    plt.imshow(screenshot_rgb)
    plt.title('Screenshot with partial image is Highlighted')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(image_rgb)
    plt.title('Partial image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# Function to capture screenshot of local HTML file using Playwright
def capture_screenshot_of_local_html(html_file_path, screenshot_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the local HTML file
        page.goto(f'file://{html_file_path}')
        
        # Capture screenshot
        page.screenshot(path=screenshot_path)
        
        browser.close()

# Example usage
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    html_file_path = os.path.join(script_dir, "index.html")  # Relative path to index.html
    screenshot_path = "screenshot.png"
    image_path = "partial_image.png"  # Adjust this path to the image you want to find

    capture_screenshot_of_local_html(html_file_path, screenshot_path)
    find_and_display_image_in_screenshot(screenshot_path, image_path)
