import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from django.contrib.staticfiles.templatetags.staticfiles import static
import numpy as np
import random
import os
from django.conf import settings
STATIC_ROOT = settings.STATIC_ROOT
mat_i = 14
mat_j = 14

def mergeImageHorizontally(image1,image2):
    """
        Merge two images into one, displayed img1 on left of img2
        :param img1: path to first image file
        :param img2: path to second image file
        :return: the merged Image object
    
    """    
    (width1, height1) = image1.size
    (width2, height2) = image2.size 
    
    result_width = width1 + width2
    result_height = max(height1, height2)    

    result = Image.new('RGBA', (result_width,result_height))
    
    result.paste(im=image1, box=(0, 0), mask=0)
    result.paste(im=image2, box=(width1, 0), mask=0)    
    
    return result

def mergeImageVertically(image1,image2):
    """
        Merge two images into one, displayed img1 on top of img2
        :param img1: path to first image file
        :param img2: path to second image file
        :return: the merged Image object
    """    
    (width1, height1) = image1.size
    (width2, height2) = image2.size 
    
    result_width = max(width1, width2)
    result_height = height1 + height2
    
    result = Image.new('RGBA', (result_width,result_height))
    
    result.paste(im=image1, box=(0, 0), mask=0)
    result.paste(im=image2, box=(0, height1), mask=0)    
    
    return result

#raw_image_path = 'raw_image/'
current_path = os.path.dirname(os.path.realpath(__file__))
raw_image_path = os.path.join(current_path , 'static' ,'css_sprites' , 'image' , 'raw')
raw_image_path = raw_image_path + "/"
#image_file_names = {0:'0.png',1:'1.png',2:'2.png',3:'3.png',4:'4.png',5:'5.png',6:'6.png',7:'7.png',8:'8.png',9:'9.png',-1:'gap.png'}
image_file_names = {0:'test0.png',1:'test1.png',2:'test2.png',3:'test3.png',4:'test4.png',5:'test5.png',6:'test6.png',7:'test7.png',8:'test8.png',9:'test9.png', -1 :'gap.png', 10 : 'test-.png' , 11 : 'test+.png', 12 : 'test,.png' , 13 : 'tests.png'}

rotations = [90,180,270,360]

def generateRandomMatrix():
    """
        Creates a random 10x10 matrix, each row having exactly once each digit
        :return: the generated matrix
    """    
    arr = np.remainder(np.arange(mat_i * mat_j),mat_i)
    arr = arr.reshape(mat_i,mat_j)
    np.apply_along_axis(np.random.shuffle, 1 , arr)    
    return arr

def generateSprite(img_name):
    arr = generateRandomMatrix()
    img = Image.new('RGBA', (0,0))
    css = []
    for row in arr:
        img_row = Image.new('RGBA', (0,0))
        css_row = []
        old_cold_width,old_col_height = img.size
        for el in row:
            im_el = Image.open(raw_image_path+image_file_names[el])
            im_el.thumbnail(tuple(i / 1 for i in im_el.size), Image.ANTIALIAS)
            idx = random.randint(0, 3)
            idx = 3
            width_of_el,height_of_el = im_el.size
            im_el = im_el.rotate(angle=rotations[idx],expand=False)
            old_row_width, old_row_height = img_row.size
            img_row = mergeImageHorizontally(img_row, im_el)
            new_row_width, new_row_height = img_row.size
            css_row.append((old_row_width, old_col_height , width_of_el , height_of_el, rotations[idx]))
            
        img = mergeImageVertically(img, img_row)
        css.append(css_row)
    img.save(os.path.join(current_path ,'static', 'css_sprites' , 'image' , 'generated' , img_name))
    return (css, arr,''+img_name)
