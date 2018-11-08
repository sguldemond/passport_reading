from PIL import Image
from cStringIO import StringIO
from shutil import copyfileobj
import os, base64

def convert_image(img_data, output_name, output_format, output=True):
    with open('tmp.jp2', 'wb') as input:
        input.write(img_data)
    
    main_img = Image.open('tmp.jp2')
    os.remove('tmp.jp2')
    
    main_img = main_img.resize(((main_img.size[0] / 2), (main_img.size[1] / 2)), Image.ANTIALIAS)

    # output_format = 'jpeg'
    buffer = StringIO()
    main_img.save(buffer, format=output_format)
    base64_image = base64.b64encode(buffer.getvalue())

    if output:
        output_folder = 'output'
        file = '{0}/{1}.{2}'.format(output_folder, output_name, output_format)

        with open(file, 'w') as output:
            buffer.seek(0)
            copyfileobj(buffer, output)
        
    buffer.close()
    return base64_image