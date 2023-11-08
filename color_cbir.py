from PIL import Image

def rgb_of_image(img_path, x, y):
    img = Image.open(img_path).convert('RGB')
    r, g, b = img.getpixel((x,y))
    a = (r,g,b)
    return a

img_path = 'photo-1579353977828-2a4eab540b9a.webp'
print(rgb_of_image(img_path, 1,1))
