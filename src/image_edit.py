#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from PIL import Image

accepted_formats = [\
    ".gif", \
    ".jpg", ".jpeg", ".jfif", ".jfi", ".jp2", ".j2c", \
    ".png", \
    ".tiff", ".tif", \
    ".webp", \
    ".bmp"
]

class ImageFactory(object):
    def __init__(self, file):
        super(ImageFactory, self).__init__()
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
                img = Image.open(srcfile)
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
                img = Image.open(srcfile)
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
        print("'concatenate_h' called")
        file = self.file
        if not len(file) > 1:
            print("requires more than 2 images.")
        else:
            pass

        f, e = os.path.splitext(file[0])

        if direction == "horizontal":
            dstfile = f + "_h.png"

            print("create 'canvas'")
            h = min(Image.open(f).size[1] for f in file)
            w_list = []
            for srcfile in file:
                img = Image.open(srcfile)
                img.thumbnail((img.size[0], h))
                w_list.append(img.size[0])
            w = sum(w_list)
            canvas = Image.new("RGBA", (w, h))
            print("canvas size:", canvas.size)

            print("paste 'img' to 'canvas'")
            pos_x = 0
            try:
                for srcfile in file:
                    img = Image.open(srcfile)
                    img.thumbnail((img.size[0], h))
                    print(os.path.basename(srcfile)+":", img.size)
                    canvas.paste(img, (pos_x, 0))
                    pos_x += img.size[0]
                canvas.save(dstfile, "PNG")
                # canvas.show()
                print("'concatenate_horizontal' finished")
            except IOError:
                print("cannot 'concatenate_horizontal'", srcfile)

        elif direction == "vertical":
            dstfile = f + "_v.png"
            print("create 'canvas'")
            w = min(Image.open(f).size[0] for f in file)
            h_list = []
            for srcfile in file:
                img = Image.open(srcfile)
                img.thumbnail((w, img.size[1]))
                h_list.append(img.size[1])
            h = sum(h_list)
            canvas = Image.new("RGBA", (w, h))
            print("canvas size:", canvas.size)

            print("paste 'img' to 'canvas'")
            pos_y = 0
            try:
                for srcfile in file:
                    img = Image.open(srcfile)
                    img.thumbnail((w, img.size[0]))
                    print(os.path.basename(srcfile)+":", img.size)
                    canvas.paste(img, (0, pos_y))
                    pos_y += img.size[1]
                canvas.save(dstfile, "PNG")
                # canvas.show()
                print("'concatenate_vertical' finished")
            except IOError:
                print("cannot 'concatenate_vertical'", srcfile)
        else:
            print("choose 'horizontal' or 'vertical'")

    def pngquant(self):
        print("'pngquant' called")
        pq = "resources\\pngquant\\pngquant.exe"
        op = " --force --ext _256.png 256 "
        file = self.file
        for srcfile in file:
            print(srcfile)
            try:
                cmd = pq + op + srcfile
                os.system(cmd)
                print("'pngquant' finished")
            except IOError:
                print("cannot convert with pngquant", srcfile)
