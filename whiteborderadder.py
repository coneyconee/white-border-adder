from PIL import Image

srcpath = input('source directory: ')
destpath = input('destination directory: ')

canvash, canvasw = int(input('canvas height: ')), int(input('canvas width: '))
bordersize = int(input('border size (try 7 for a start): ')) * 10

src = input('source: ')

srcimg = Image.open(src)

imgmaxh, imgmaxw = canvash - 2 * bordersize, canvasw - 2 * bordersize

srcimg.thumbnail((imgmaxw, imgmaxh))

canvas = Image.new("RGB", (canvasw,canvash), "white")

x, y = (canvasw - srcimg.width) // 2, (canvash - srcimg.height) // 2

canvas.paste(srcimg, (x, y))

canvas.save(destpath, "JPEG")

print(f"saved: {destpath}")

