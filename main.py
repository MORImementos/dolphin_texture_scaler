import os
from PIL import Image
import json
import fnmatch

original_images = []
new_images = []

##### MAKE SURE YOU HAVE THESE FOLDER NAMES #####
orig_path = "original_images/"
new_path = "new_images/"
output_path = "output/"
make_transparent_path = "make_transparent/"

##### ADJUST MAX WIDTH AND HEIGHT HERE #####
MAX_WIDTH = 4000
MAX_HEIGHT = 4000

##### ADJUST MULTIPLIER FOR IMAGE SCALING HERE #####
multiplier = 10

##### FOLLOW THE PATTERN IN THE JSON FILE TO ADD NEW NAMES. YOU CAN NAME THE NEW FILE THE KEYWORD AND THE SCRIPT WILL
##### AUTOMATICALLY RENAME IT FOR YOU. YOU CAN ALSO NAME IT THE TARGET FILENAME, THIS IS JUST FOR CONVENIENCE.
with open("image_key.json") as dt:
    keywords = json.load(dt)
    # todo: maybe a way to automatically loop through them in a particular order


# get all filenames in a directory (in this case, the original images and the new images)
def get_filenames(directory):
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def get_unique_filenames(output_path, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(output_path, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


# find instances where the new files and the original files match (to know which ones are going to be used)
def find_matches(orig_images, new_images):
    return set(orig_images) & set(new_images)


# get the size values for the files
def get_image_sizes(path, matches):
    size_dict = {filename: () for filename in matches}
    for filename in matches:
        with Image.open(os.path.join(path, filename)) as im:
            size_dict[filename] = im.size
    return size_dict


# resize the new images for better quality while converting them to the aspect ratio of the original files
def resize_new_images(orig_sizes, new_images, keywords, multiplier=10):
    # make output path if there isn't one
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # iterate over keywords in json file
    for keyword, orig_filename in keywords.items():
        # if the filename is in the keywords, extract the width and height. check for existence of keyword-named image
        if orig_filename in orig_sizes:
            orig_width, orig_height = orig_sizes[orig_filename]
            keyword_file = f"{keyword}.png"
            # if keyword-named image in files
            if keyword_file in new_images:
                new_file = keyword_file

            # else if the image has the same name as original file
            elif orig_filename in new_images:
                new_file = orig_filename
            # Find all files in new_images that contain the keyword
            # matching_files = fnmatch.filter(new_images, f"*{keyword}*")
            # open image
            with Image.open(os.path.join(new_path, new_file)) as im:
                print(f"Resizing {new_file}. . .")
                needs_resize = True
                # check to be sure that the image is not resized to be too large
                while needs_resize:
                    target_width = orig_width * multiplier
                    target_height = orig_height * multiplier

                    # if under max w/h, save file to output folder
                    if target_width <= MAX_WIDTH and target_height <= MAX_HEIGHT:
                        resized = im.resize((target_width, target_height))
                        resized.save(os.path.join(output_path, orig_filename))
                        if new_file == keyword_file:
                            print(f"{new_file} has been resized and renamed to {orig_filename} ({im.size[0]}x{im.size[1]} -> {resized.size[0]}x{resized.size[1]})")
                        else:
                            print(f"New {new_file} has been resized to ({im.size[0]}x{im.size[1]} -> {resized.size[0]}x{resized.size[1]})")

                        needs_resize = False
                    # if too big, decrement multiplier by 1 and repeat
                    else:
                        print(f"Multiplier of {multiplier} exceeds {MAX_WIDTH}x{MAX_HEIGHT}. Resizing with multiplier of {multiplier - 1}. . .")
                        multiplier -= 1


def make_images_transparent(transparent_sizes, transparent_images):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in transparent_images:
        # print(filename, orig_sizes)
        # this logic should likely be more fleshed out, but for now, it will just automatically include this in the new,
        # without need for the original file. todo: filename validation of some form
        # if filename in orig_sizes:
        trans_width, trans_height = transparent_sizes[filename]
        transparent_img = Image.new("RGBA", (trans_width, trans_height), (0, 0, 0 ,0))
        transparent_img.save(os.path.join(output_path, filename))
        print(f"{filename} made transparent.")

if __name__ == "__main__":
    original_images = get_filenames(orig_path)
    new_images = get_filenames(new_path)
    transparent_images = get_filenames(make_transparent_path)

    orig_sizes = get_image_sizes(orig_path, original_images)
    new_sizes = get_image_sizes(new_path, new_images)
    transparent_sizes = get_image_sizes(make_transparent_path, transparent_images)

    resize_new_images(orig_sizes, new_images, keywords, multiplier=multiplier)
    make_images_transparent(transparent_sizes, transparent_images)

