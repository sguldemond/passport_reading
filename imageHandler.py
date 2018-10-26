from pgmagick import Image
import os

# print(pgmagick.gminfo.version)

def convert_image(img_data, file_name):
    print "Creating tmp file..."
    face_img = open("tmp.jp2", "wb")
    face_img.write(img_data)
    face_img.close()

    img = Image('tmp.jp2') # Input Image

    output_type = '.png'
    print "Converting jp2 to png image..."
    img.write("output/" + file_name + output_type)

    os.remove("tmp.jp2")