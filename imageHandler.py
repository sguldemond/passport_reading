from pgmagick import Image
import os, base64

# print(pgmagick.gminfo.version)

def convert_image(img_data, file_name):
    print "Creating tmp file..."
    face_img = open("tmp.jp2", "wb")
    face_img.write(img_data)
    face_img.close()

    img = Image('tmp.jp2') # Input Image

    output_type = '.jpg'
    print("Converting jp2 to {} image...".format(output_type))
    file = "output/" + file_name + output_type
    img.write(file)
    os.remove("tmp.jp2")

    with open(file, 'r') as input:
        base64_image = base64.b64encode(input.read())
    
    # print(base64_image)
    
    return base64_image