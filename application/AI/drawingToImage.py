import numpy as np
from PIL import Image

def drawing_to_image(self, drawing):
    # Create a blank 256x256 image
    img_size = 256
    image = np.zeros((img_size, img_size), dtype=np.uint8)
    
    # Find bounding box
    all_x = []
    all_y = []
    
    for stroke in drawing:
        x_coords = stroke[0]
        y_coords = stroke[1]
        all_x.extend(x_coords)
        all_y.extend(y_coords)

    if not all_x or not all_y:
        return image  # Return blank if no valid drawing data

    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)

    # Normalize strokes to fit within bounding box
    for stroke in drawing:
        x_coords = np.array(stroke[0])
        y_coords = np.array(stroke[1])
        
        x_coords = (x_coords - x_min).astype(int)
        y_coords = (y_coords - y_min).astype(int)

        for i in range(len(x_coords) - 1):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i + 1], y_coords[i + 1]
            image[y1, x1] = 255
            image[y2, x2] = 255

    # Crop the drawing to the bounding box
    cropped_image = image[y_min:y_max + 1, x_min:x_max + 1]

    # Resize the cropped image to 256x256
    pil_image = Image.fromarray(cropped_image)
    pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)
    
    return np.array(pil_image)
