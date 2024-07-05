#  Find partial image in the given screenshot

## Step 1: Install Required Packages

1.1 Clone the repo using below URL

```bash
https://github.com/ceiqapractice/PartialImageComp.git

1.2 Install Required Packages:

```bash
pip install playwright opencv-python-headless matplotlib
```

## Step 2: Creating Your Python Script

Here’s how you can update your script to perform manual pixel comparison:

capture_and_match_image.py

```py
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
    plt.title('Screenshot with partial Highlighted')
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
    html_file_path = r"C:\Users\dganesh\OneDrive - Computer Enterprises Inc\Desktop\Comp\index.html"  # Adjust this path to your local HTML file
    screenshot_path = "screenshot.png"
    image_path = "partial_image.png"  # Adjust this path to the image you want to find

    capture_screenshot_of_local_html(html_file_path, screenshot_path)
    find_and_display_image_in_screenshot(screenshot_path, image_path)


```

## Explanation

find_and_display_image_in_screenshot(screenshot_path, image_path):

This function reads the screenshot and image template using OpenCV (cv2.imread).
Converts the images to RGB format using cv2.cvtColor for compatibility with Matplotlib.
Performs template matching using cv2.matchTemplate and identifies the matched area above a specified threshold (threshold = 0.8).
Draws rectangles around matched areas in the screenshot using cv2.rectangle.
Displays the original screenshot with the matched area highlighted alongside the image template using Matplotlib (plt.imshow).
capture_screenshot_of_local_html(html_file_path, screenshot_path):

Uses Playwright to launch a Chromium browser, navigate to a local HTML file (file:// URL), and capture a screenshot of the page.
Saves the screenshot to screenshot_path.
Example Usage (if __name__ == "__main__":):

Defines paths for html_file_path, screenshot_path, and image_path.
Calls capture_screenshot_of_local_html to capture a screenshot of the local HTML file.
Calls find_and_display_image_in_screenshot to check if the specified image template (image_path) is present in the captured screenshot (screenshot_path) and visually displays the result.

## Running Your Script

Navigate to your project directory in the terminal.

```bash
python capture_and_match_image.py
```

## Review the Output:

The script will launch a Chromium browser, load the specified HTML file, capture a screenshot, perform template matching with the specified image template, and display the visual result using Matplotlib.

![image](https://github.com/ceiqapractice/PartialImageComp/assets/110914539/e7d043cb-bcb6-4163-b7b5-8f0b1ca938e4)

