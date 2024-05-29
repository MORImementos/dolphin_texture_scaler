# Usage:
- Put original textures into the original_images folder.
- Put the new images you want to replace them with into the new_images folder. They *must* either match the filename of the original image they are replacing, or match the keyword associated with the original file (more below).
- In the main.py file, adjust any parameters you may need (maximum width, maximum height, multiplier for resizing).
- run `python main.py` and the new files should be added to your output folder.

## image_key.json
This is ofor the sake of avoiding any potential need to copy/paste/rename files. Instead, you can associate an original file with a keyword, as demonstrated in the json file, and if the new image is named `{keyword}.png`, it will correctly identify it and rename it.