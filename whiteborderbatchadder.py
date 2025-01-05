import os
from PIL import Image

srcdir = input('source directory: ')
destdir = input('destination directory: ')

os.makedirs(destdir, exist_ok=True)

canvash, canvasw = int(input('canvas height: ')), int(input('canvas width: '))
bordersize = int(input('border size (try 7 for a start): ')) * 10

for file in os.listdir(srcdir):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        srcpath = os.path.join(srcdir, file)
        destpath = os.path.join(destdir, f"border_{file}")
        
        srcimg = Image.open(srcpath)

        imgmaxh, imgmaxw = canvash - 2 * bordersize, canvasw - 2 * bordersize

        srcimg.thumbnail((imgmaxw, imgmaxh))

        canvas = Image.new("RGB", (canvasw,canvash), "white")

        x, y = (canvasw - srcimg.width) // 2, (canvash - srcimg.height) // 2

        canvas.paste(srcimg, (x, y))

        canvas.save(destpath, "JPEG")

        print(f"saved: {destpath}")

print('all images saved in destination directory')