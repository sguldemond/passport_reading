from pgmagick import Image
import os, base64

def convert_image(img_data, output_name, output=True):
    temp_img = open("tmp.jp2", "wb") # wb = write in binary
    temp_img.write(img_data)
    temp_img.close()

    main_img = Image('tmp.jp2') # input tmp image file
    os.remove("tmp.jp2") # no need for temp file

    file_type = 'jpg'
    print("Converting jp2 to {} image...".format(file_type))

    output_folder = "output"
    file = "{0}/{1}.{2}".format(output_folder, output_name, file_type)
    
    main_img.write(file)

    with open(file, 'r') as input:
        base64_image = base64.b64encode(input.read())
        
    if output == False:
        os.remove(file)
    
    return base64_image