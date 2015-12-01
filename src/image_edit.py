#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from PIL import Image

accepted_formats = [
    ".gif",
    ".jpg", ".jpeg", ".jfif", ".jfi", ".jp2", ".j2c",
    ".png",
    ".tiff", ".tif",
    ".webp",
    ".bmp"
]

class ImageFactory():
    def __init__(self, file):
        super().__init__()
        print("'ImageFactory' called")
        self.file = file
        for srcfile in self.file:
            f, e = os.path.splitext(srcfile)
            if e.lower() in accepted_formats:
                print("file is in 'accepted_formats'")
            else:
                print("cannot open", srcfile)
                print("accepted_formats:", accepted_formats)

    def resize(self, half, x, y):
        print("'resize' called")
        file = self.file
        for srcfile in file:
            f, e = os.path.splitext(srcfile)
            dstfile = f + "_t.png"
            try:
                with Image.open(srcfile) as img:
                    print("original size:", img.size)
                    if half:
                        x = img.size[0]/2
                        y = img.size[1]/2
                        size = (x, y)
                    else:
                        size = (x, y)
                    img.thumbnail(size)
                    img.save(dstfile, "PNG")
                    # img.show()
                    print("'resize' finished")
                    print("resized:", img.size)
            except IOError:
                print("cannot resize", srcfile)

    def rotate(self, direction):
        print("'rotate' called")
        file = self.file
        for srcfile in file:
            f, e = os.path.splitext(srcfile)
            try:
                with Image.open(srcfile) as img:
                    if direction == "right":
                        print("'direction' is 'right'")
                        dstfile = f + "_r.png"
                        img.transpose(Image.ROTATE_270).save(dstfile, "PNG")
                        # img.transpose(Image.ROTATE_270).show()
                        print("'rotate_right' finished")
                    elif direction == "left":
                        print("'direction' is 'left'")
                        dstfile = f + "_l.png"
                        img.transpose(Image.ROTATE_90).save(dstfile, "PNG")
                        # img.transpose(Image.ROTATE_90).show()
                        print("'rotate_left' finished")
                    else:
                        print("choose 'right' or 'left'")
            except IOError:
                print("cannot rotate", srcfile)

    def concatenate(self, direction):
        print("'concatenate' called")
        file = self.file
        print("file:", file)

        if direction == "horizontal":
            print("horizontal")
            f, e = os.path.splitext(file[0])
            dstfile = f + "_h.png"
            print("dstfile:", dstfile)
            min_height = min(Image.open(i).size[1] for i in file)
            print("min_height:", min_height)

            width_list = []
            for i in file:
                with Image.open(i) as img:
                    size = (img.size[0], min_height)
                    img.thumbnail(size)
                    width_list.append(img.size[0])
                    print("width_list:", width_list)
            sum_width = sum(width_list)
            canvas_size = (sum_width, min_height)
            canvas = Image.new("RGBA", canvas_size)
            print("canvas.size:", canvas.size)
            # canvas.show()

            pos_x = 0
            try:
                for i in file:
                    with Image.open(i) as img:
                        size = (img.size[0], min_height)
                        img.thumbnail(size)
                        print("img.size", img.size)
                        canvas.paste(img, (pos_x, 0))
                        pos_x += img.size[0]
                # canvas.show()
                canvas.save(dstfile, "PNG")
            except IOError:
                print("cannot 'concatenate_horizontal'", i)

        elif direction == "vertical":
            print("vertical")
            f, e = os.path.splitext(file[0])
            dstfile = f + "_v.png"
            print("dstfile:", dstfile)
            min_width = min(Image.open(i).size[0] for i in file)
            print("min_width:", min_width)

            height_list = []
            for i in file:
                with Image.open(i) as img:
                    size = (min_width, img.size[1])
                    img.thumbnail(size)
                    height_list.append(img.size[1])
                    print("height_list:", height_list)
            sum_height = sum(height_list)
            canvas_size = (min_width, sum_height)
            canvas = Image.new("RGBA", canvas_size)
            print("canvas.size:", canvas.size)

            pos_y = 0
            try:
                for i in file:
                    with Image.open(i) as img:
                        size = (min_width, img.size[1])
                        img.thumbnail(size)
                        print("img.size:", img.size)
                        canvas.paste(img, (0, pos_y))
                        pos_y += img.size[1]
                # canvas.show()
                canvas.save(dstfile, "PNG")
            except IOError:
                print("cannot 'concatenate_vertical'", i)

        else:
            print("choose 'horizontal' or 'vertical'")

    def pngquant(self):
        print("'pngquant' called")
        pq = "resources\\pngquant\\pngquant.exe"
        op = " --force --verbose --ext _256.png 256 "
        file = self.file
        for srcfile in file:
            print(srcfile)
            try:
                cmd = pq + op + srcfile
                os.system(cmd)
            except IOError:
                print("cannot convert with pngquant", srcfile)
        print("'pngquant' finished")
