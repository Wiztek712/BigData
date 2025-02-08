import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from PIL import Image
import pandas as pd
import ujson as json

class QuickDrawDataset(Dataset):
    def __init__(self, drawings, labels, resize_to=(64, 64)):
        """
        Args:
            drawings (list or array): List of drawing data (tensor or numpy arrays).
            labels (list or array): List of class labels corresponding to each drawing.
            resize_to (tuple): Target size for resizing the image.
        """
        self.drawings = drawings
        self.labels = labels
        self.resize_to = resize_to  # Tuple (width, height)

    def __len__(self):
        return len(self.drawings)

    def __getitem__(self, idx):
        # Convert the drawing format to image
        drawing = self.drawings.iloc[idx] if isinstance(self.drawings, pd.Series) else self.drawings[idx]
        image = self.drawing_to_image(drawing)
        label = self.labels.iloc[idx] if isinstance(self.labels, pd.Series) else self.labels[idx]
        
        # Convert the image to a tensor and add batch dimension
        image_tensor = torch.FloatTensor(image).unsqueeze(0)
        return image_tensor, label

    def drawing_to_image(self, drawing):
        img_size = 64
        image = np.zeros((512, 512), dtype=np.uint8)
        
        all_x, all_y = [], []
        
        for stroke in drawing:
            all_x.extend(stroke[0])
            all_y.extend(stroke[1])

        # print("all_x : ", all_x)
        # print("all_y : ",all_y)

        if not all_x or not all_y:
            return image  # Return blank if no valid drawing data

        # Find bounding box
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)

        # print("max_x : ", x_max, " min_x : ", x_min)
        # print("max_y : ", y_max, " min_y : ", y_min)

        width = x_max - x_min
        height = y_max - y_min
        longest_side = max(width, height)

        # print("longest_side : ", longest_side)

        # Compute center of drawing
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2

        # Compute new square bounds while keeping it within 256x256
        half_size = longest_side / 2
        x_start = max(0, min(512 - longest_side, int(x_center - half_size)))
        y_start = max(0, min(512 - longest_side, int(y_center - half_size)))
        x_end = min(512, x_start + longest_side)
        y_end = min(512, y_start + longest_side)

        # Normalize strokes within the centered bounding box
        for stroke in drawing:
            x_coords = np.array(stroke[0])
            y_coords = np.array(stroke[1])

            # Shift points to align with the new bounding box
            x_coords = np.clip(x_coords - (x_center - half_size), 0, longest_side - 1)
            y_coords = np.clip(y_coords - (y_center - half_size), 0, longest_side - 1)

            for i in range(len(x_coords) - 1):
                x1, y1 = int(x_coords[i]), int(y_coords[i])
                x2, y2 = int(x_coords[i + 1]), int(y_coords[i + 1])

                # Draw the strokes on the image
                if 0 <= x1 < longest_side and 0 <= y1 < longest_side:
                    image[y1 + y_start, x1 + x_start] = 255
                if 0 <= x2 < longest_side and 0 <= y2 < longest_side:
                    image[y2 + y_start, x2 + x_start] = 255

        # Extract the centered square region
        cropped_image = image[y_start:y_end, x_start:x_end]

        # Resize to 64x64
        pil_image = Image.fromarray(cropped_image)
        pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)

        return np.array(pil_image)
    
def process(data):
    try:
        print("Processing data...")
        # print(data)
        df = pd.DataFrame.from_records(data)
        # print("df : ", df)
        prediction_dataset = QuickDrawDataset(df["drawing"], df["word"], resize_to=(64, 64))
        # print("prediction_dataset : ", prediction_dataset)
        data_loader = DataLoader(prediction_dataset, batch_size=1, shuffle=False)
        # print("data_loader : ", data_loader)
        return data_loader
    except Exception as e:
        return {"error": str(e)}


