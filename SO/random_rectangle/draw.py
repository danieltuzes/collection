from PIL import Image, ImageDraw
import random

piece = 0
while (piece < 100):
    with Image.open("base.png").convert("RGBA") as source_img:
        height = 100  # you could read this from the input image base.png
        width = 100  # you could read this too from the input image base.png
        draw = ImageDraw.Draw(source_img)
        while (width > 0):
            while (height > -1):
                color = random.randint(1, 3)
                if (color == 1):
                    R = 255
                    G = 0
                    B = 0
                elif (color == 2):
                    R = 0
                    G = 255
                    B = 0
                elif (color == 3):
                    R = 0
                    G = 0
                    B = 255

                draw.rectangle(((height, 0), (height, width)), fill=(R, G, B))
                height -= 1
            width -= 1
            height = 100
        # if you want a double loop, this is style more common:
        # for w in range(0,weight):
        #   for h in range(0,height):
        piece += 1
        source_img .save("images/" + str(piece) + ".png", "PNG")

print("Images is done!")
