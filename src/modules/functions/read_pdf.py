from pdf2image import convert_from_path, convert_from_bytes
import tempfile
import cv2
import os.path

from .. img_processing.image_processor import Image_Processor

TEMP_IMG_FILE_NAME = "tmp_img_file_"

def read_pdf(input_file):
  with tempfile.TemporaryDirectory() as path:
    # set path to tmp image
    img_file_path = os.path.join(path, TEMP_IMG_FILE_NAME + ".jpg")
    # convert given pdf to an image
    converted_imgs = convert_from_path(input_file)
    converted_imgs[0].save(img_file_path, 'JPEG')

    # open and display image
    Img = Image_Processor(img_file_path)
    data = Img.get_numerical_data(show=True)
    # print(data)
    # cv2.destroyAllWindows()
  return data