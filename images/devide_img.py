from pathlib import Path

import cv2
import numpy as np

img = cv2.imread("charall.png")

rows = 4
cols = 3

chunks = []
for row_img in np.array_split(img, rows, axis=0):
    for chunk in np.array_split(row_img, cols, axis=1):
        chunks.append(chunk)

# Save
output_dir = Path("moving")
output_dir.mkdir(exist_ok=True)
for i, chunk in enumerate(chunks):
    save_path = output_dir / f"moving_{i:02d}.png"
    cv2.imwrite(str(save_path), chunk)
