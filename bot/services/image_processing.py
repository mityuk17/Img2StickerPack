from PIL import Image
import os


class ImageProcessor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.img = Image.open(image_path)
        self.img_to_square_resolution()
        
    
    @property
    def img_size(self):
        return self.img.size[0]
        
        
    def img_to_square_resolution(self):
        width, height = self.img.size
        
        size = min(width, height)
        
        left_upper_x = (width - size) // 2
        right_lower_x = left_upper_x + size
        left_upper_y = (height - size) // 2
        right_lower_y = left_upper_y + size
        
        self.img = self.img.crop(box=(left_upper_x, left_upper_y, right_lower_x, right_lower_y))
        
    
    def get_square_part(self, square_x: int, square_y: int, N: int) -> Image.Image:
        square_size = self.img_size // N
        
        left_upper_x = square_x * square_size
        right_lower_x = (square_x + 1) * square_size
        right_lower_y = (square_y + 1) * square_size
        left_upper_y = square_y * square_size
        
        square = self.img.crop((left_upper_x, left_upper_y, right_lower_x, right_lower_y)).resize((512, 512))
        
        return square
        
    
    def cut_img_to_squares(self, N: int) -> list[Image.Image]:
        square_parts = []
        for square_y in range(N):
            for square_x in range(N):
                square_parts.append(self.get_square_part(square_x, square_y, N))
        
        return square_parts
    
    
    def get_cut_image(self, request_id: str):
        N = 5
        squares = self.cut_img_to_squares(N)
        os.mkdir(f"images/processed/{request_id}")
        all_paths = []
        for i in range(len(squares)):
            filename = f"images/processed/{request_id}/{i}.png"
            squares[i].save(filename)
            all_paths.append(filename)
            
        return all_paths