import argparse
from glob import glob
import Image


# Arg Parser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode"          , required= False , default= "sticker"   , type= str           , help= 'Input path\ne.g., "sticker"')
ap.add_argument("-i", "--input"         , required= False , default= "./original", type= str           , help= "Input path\ne.g., ./original")
ap.add_argument("-t", "--type"          , required= False , default= "png"       , type= str           , help= "Format of the images\ne.g., png")
ap.add_argument("-p", "--padding"       , required= False , default= 0           , type=int , help= "add padding to the image")
ap.add_argument("-s", "--output-size"   , required= False , default= (512, 128)  , nargs=2, type=int , help= "(width, height) of the image\ne.g., (512, 128)")
output_path = f"{vars(ap.parse_args())['input']}_{vars(ap.parse_args())['output_size'][0]}x{vars(ap.parse_args())['output_size'][1]}"
ap.add_argument("-o", "--output"        , required= False , default= output_path , type= str           , help= "Output path\ne.g., ./512x128")
ap.add_argument("--exclude-sub-folder"  , required= False , default= "Animated"  , type= str           , help= "Exclude directories\ne.g., Animated")
ap.add_argument("--trim-transparent"    , required= False , default= True        , type= bool          , help= "Trim transparent rows & columns")
ap.add_argument("--center"              , required= False , default= False       , type= bool          , help= "center image in the canvas")

# Constants
STICKER_SIZE = 512
EMOJI_SIZE = 100

# Variables
args = vars(ap.parse_args())

mode         = args["mode"]                      # "sticker" or "emoji"
input_path   = args["input"].replace("\\", "/")  # "./original"
output_path  = args["output"].replace("\\", "/") # "./512x128"
image_format = args["type"]                      # "png"
output_size  = args["output_size"]               # (width, heigth)
padding      = args["padding"]                   # 10

if mode == "sticker":
    if STICKER_SIZE not in output_size:
        raise ValueError(f"One of the dimensions should be {STICKER_SIZE}")
    size_scale, axis = (output_size[0], 0) if output_size[0] != STICKER_SIZE else (output_size[1], 1)

elif mode == "emoji":
    if EMOJI_SIZE not in output_size:
        raise ValueError(f"One of the dimensions should be {EMOJI_SIZE}")
    size_scale, axis = (output_size[0], 0) if output_size[0] != EMOJI_SIZE else (output_size[1], 1)

else:
    raise ValueError('argument <mode> should be "sticker" or "emoji"')


images_address = glob(pathname= f"{input_path}/**/*.{image_format}", recursive= True, include_hidden= True)

for path in images_address:
    path = path.replace("\\", "/")

    # Skip paths which contain a specific name.
    if args["exclude_sub_folder"] in path:
        continue
    
    img = Image.Open(path= path, format= image_format, output_size= output_size, size_scale= size_scale)

    if args["trim_transparent"]:
        img.trim_transparent()
    
    if img.image.size != size_scale:
        img.resize(axis= axis, padding= padding)
    
    img.save(input_path= input_path, output_path= output_path, center= args["center"])