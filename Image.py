from PIL import Image as Img
from pathlib import Path



class Open:
    def __init__(self, path: str, format: str, output_size: tuple, size_scale= int) -> None:
        self.path = path
        self.format = format.lower()
        self.image = Img.open(fp= path)
        self.output_size = output_size
        self.size_scale = size_scale

    def trim_transparent(self):
        self.image = self.image.crop(box= self.image.getbbox())

    def resize(self, axis: int, padding: int): # axis=0 (width) , axis=1 (heigth)
        image_width  = int((self.image.size[0] / self.image.size[axis]) * self.size_scale)
        image_heigth = int((self.image.size[1] / self.image.size[axis]) * self.size_scale)

        # if the other axis goes out of range, then the <axis> is <1 - axis>
        if image_width > self.output_size[0] or image_heigth > self.output_size[1]:
            image_width  = int((self.image.size[0] / self.image.size[1 - axis]) * self.size_scale)
            image_heigth = int((self.image.size[1] / self.image.size[1 - axis]) * self.size_scale)

        # Down-Scaling
        if self.image.size[0] > image_width:
            self.image = self.image.resize(size= (image_width - 2*padding, image_heigth - 2*padding), resample= Img.Resampling.LANCZOS)
        
        # Upscaling
        else:
            self.image = self.image.resize(size= (image_width, image_heigth), resample= Img.Resampling.LANCZOS)
        

    def save(self, input_path:str, output_path: str, center: bool):
        output_path = "/".join(self.path.split("/")[:-1]).replace(input_path, output_path)
        output_image_name = self.path.split("/")[-1]
        
        # create folders if not exist
        Path(output_path).mkdir(parents=True, exist_ok=True)

        if self.format in ["png", "webp"]:
            mode = "RGBA"
        else:
            mode = "RGB"

        canvas = Img.new(size= self.output_size, mode= mode)
        if center:
            width_pos = (self.output_size[0] - self.image.size[0]) // 2
            heigth_pos = (self.output_size[1] - self.image.size[1]) // 2
        else:
            width_pos = 0
            heigth_pos = 0
        canvas.paste(self.image, box= (width_pos, heigth_pos))

        canvas.save(fp= f"{output_path}/{output_image_name}", optimize= True, compress_level= 9)