from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

img = Image.open("hlebushek.png").convert("L")

font = ImageFont.truetype("YesevaOne-Regular.ttf", size=40)

draw = ImageDraw.Draw(img)
draw.text((100, 350), "ВО ВСЕ ТЯЖЕЧКИ", fill=0, font=font, stroke_width=2, stroke_fill=255)
img.show()