import fitz
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
import cv2
import os.path

from .img_processing.pre_process_img import Image_pre_processor

#! MACROS

TEMP_IMG_FILE_NAME = "tmp_img_file_"

def get_input(inps, args):
    for a in args:
        if a in inps:
            return args[a]
    print("Error getting: {}".format(inps))
    return None

def read_pdf(*args, **kwargs):

    input_file = get_input(["input_file"], args[0])


    with tempfile.TemporaryDirectory() as path:
        # set path to tmp image
        img_file_path = os.path.join(path, TEMP_IMG_FILE_NAME + ".jpg")
        # convert given pdf to an image
        converted_imgs = convert_from_path(input_file)
        converted_imgs[0].save(img_file_path, 'JPEG')

        # open and display image
        Img = Image_pre_processor(img_file_path)
        data = Img.get_numerical_data(show=True)
        print(data)


        cv2.destroyAllWindows()



    # #get document dimensions
    # input1 = PdfFileReader(open(input_file, 'rb'))
    # input1.getPage(0).mediaBox
    # height = input1.getPage(0).mediaBox.getHeight()
    # width = input1.getPage(0).mediaBox.getWidth()

    # # retrieve the first page of the PDF
    # doc = fitz.open(input_file)
    # first_page = doc[0]


    # print("input_file", input_file)

    