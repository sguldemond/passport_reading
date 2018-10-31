from PIL import Image
import os, base64

def convert_image(img_data, output_name, output=True):
    with open('tmp.jp2', 'wb') as input:
        input.write(img_data)
    
    main_img = Image.open('tmp.jp2')
    os.remove('tmp.jp2') # no need for temp file

    file_type = 'jpg'
    output_folder = 'output'
    file = '{0}/{1}.{2}'.format(output_folder, output_name, file_type)
    
    main_img.resize(((main_img.size[0] / 3), (main_img.size[1] / 3)), Image.ANTIALIAS)

    main_img.save(file)


    with open(file, 'r') as input:
        base64_image = base64.b64encode(input.read())
        
    if output == False:
        os.remove(file)
    
    return base64_image