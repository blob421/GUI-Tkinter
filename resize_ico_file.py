#MAke image compatible tinkter

from PIL import Image
import os 

icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
new_image_path = os.path.join(os.path.dirname(__file__), "favicon2.ico")

img = Image.open(icon_path)  # or your original source
img = img.resize((32, 32), Image.LANCZOS)
img.save(new_image_path, format="ICO", sizes=[(32, 32)])
