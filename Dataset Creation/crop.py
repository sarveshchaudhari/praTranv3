import cv2
import numpy as np

def crop_above_footnotes(image_path, output_path=None):
    # 1. Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not open or find the image: {image_path}")
    
    # 2. Threshold or use edge detection
    #    Here, we do a simple threshold to highlight darker text/lines
    #    You might need to invert if lines are white on black background
    _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Optional morphological dilation to make faint lines thicker
    kernel = np.ones((3, 50), np.uint8)  # (height=3, width=50) emphasizes horizontal structures
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # 3. Detect horizontal lines
    #    We can do a horizontal “scan” or use Hough transform.
    #    Below is a simpler approach: find contours and look for wide horizontal bars.
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # We’ll track the y-coord of the lowest horizontal line that’s wide enough.
    # 'wide enough' can be determined by comparing contour width to image width, etc.
    footnote_line_y = 0
    height, width = img.shape[:2]
    min_width_ratio = 0.75  # the line must be at least 75% of page width
    min_contour_width = min_width_ratio * width
    
    # Loop over contours and find the bounding rectangle of each
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # If the contour is wide (like a horizontal line) and near the bottom half
        if w > min_contour_width and y > height * 0.5:
            # Update footnote_line_y to the largest y if it's below the current stored one
            # i.e., we want the line that is furthest down on the page
            if y > footnote_line_y:
                footnote_line_y = y
    
    # If we didn’t find any line, footnote_line_y would be 0 (meaning no crop).
    # If footnote_line_y is too close to the top, we skip cropping. Adjust as needed.
    if footnote_line_y < height * 0.1:
        # No valid line found or it’s suspiciously near the top
        print("No reliable footnote line detected. Returning original image.")
        cropped = img
    else:
        # Crop from the top to just above the line
        # You might want to subtract a small margin
        margin = 5
        top_y = max(0, footnote_line_y - margin)
        cropped = img[:top_y, :]  # everything from row 0 to row top_y
    
    # Save or return the cropped image
    if output_path:
        cv2.imwrite(output_path, cropped)
    return cropped

if __name__ == "__main__":
    image_path = "image.png"
    output_path = "page_cropped.png"
    cropped_image = crop_above_footnotes(image_path, output_path)

    # From here, pass 'page_cropped.png' or 'cropped_image' to your OCR engine.
