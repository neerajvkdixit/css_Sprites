import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

import numpy as np
import random
from django.contrib.staticfiles.templatetags.staticfiles import static

#resize_height = 17
#resize_width = 8
resize_height = 22
resize_width = 9
size = resize_width,resize_height
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

    if(width2 == 1):
        result_width = width1 + 1
    else:
        result_width = width1 + resize_width
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

raw_image_path = 'static/image/raw/'
#image_file_names = {0:'0.png',1:'1.png',2:'2.png',3:'3.png',4:'4.png',5:'5.png',6:'6.png',7:'7.png',8:'8.png',9:'9.png',-1:'gap.png','space' : 'space.png'}
image_file_names = {0:'0.png',1:'1.png',2:'2.png',3:'3.png',4:'4.png',5:'5.png',6:'6.png',7:'7.png',8:'8.png',9:'9.png',-1:'gap.png','space' : 'space.png', 10 : '-.png',11 : '+.png',12 : ',.png',13 : 's.png'}
rotations = [90,180,270,360]

def generateRandomMatrix(type):
    """
        Creates a random 10x10 matrix, each row having exactly once each digit
        :return: the generated matrix
    """
    # arr = np.remainder(np.arange(100),10)
    # arr = arr.reshape(10,10)
    # np.apply_along_axis(np.random.shuffle, 1 , arr)

    is_first_horizontal = 0
    is_later_horizontal = 1
    is_first_vertical = 2
    is_later_vertical = 3



    if(type == is_first_horizontal):
        arr = np.remainder(np.arange(2 * mat_i * mat_j, step=1, dtype=np.dtype(np.int32)), mat_i)
        arr = arr.reshape(2 * mat_i, mat_j)
        np.apply_along_axis(np.random.shuffle, 1, arr)
        for i in range(2 * mat_i):
            if (i % 2 == 0):
                for j in range(mat_j):
                    arr[i][j] = -1
    elif(type == is_later_horizontal):
        arr = np.remainder(np.arange(2 * mat_i * mat_j, step=1, dtype=np.dtype(np.int32)), mat_i)
        arr = arr.reshape(2 * mat_i, mat_j)
        np.apply_along_axis(np.random.shuffle, 1, arr)
        for i in range(2 * mat_i):
            if (i % 2 == 1):
                for j in range(mat_j):
                    arr[i][j] = -1
    elif(type == is_first_vertical):
        arr = np.remainder(np.arange(2 * mat_i * mat_j, step=1, dtype=np.dtype(np.int32)), mat_i)
        arr = arr.reshape(2*mat_i, mat_j)
        np.apply_along_axis(np.random.shuffle, 1, arr)
        arr = np.transpose(arr)
        for i in range(2 * mat_i):
            if (i % 2 == 0):
                for j in range(mat_j):
                    arr[j][i] = -1
    elif(type == is_later_vertical):
        arr = np.remainder(np.arange(2 * mat_i * mat_j, step=1, dtype=np.dtype(np.int32)), mat_i)
        arr = arr.reshape(2 * mat_i, mat_j)
        np.apply_along_axis(np.random.shuffle, 1, arr)
        arr = np.transpose(arr)
        for i in range(2 * mat_i):
            if (i % 2 == 1):
                for j in range(mat_j):
                    arr[j][i] = -1

    arr1 = []
    for i in range(len(arr)):
        row = []
        for j in range(len(arr[i])):
            row.append(int(arr[i][j]))
        arr1.append(row)

    return arr1

def generateSprite(img_name,type):
    arr = generateRandomMatrix(type)
    img = Image.new('RGBA', (0,0))
    css = []
    for row in arr:
        img_row = Image.new('RGBA', (0,0))
        css_row = []
        old_cold_width,old_col_height = img.size
        for el in row:
            if(el == -1):
                for i in range(resize_width):
                    im_el = Image.open(raw_image_path + image_file_names['space'])
                    im_el.thumbnail(size, Image.ANTIALIAS)
                    img_row = mergeImageHorizontally(img_row, im_el)
            else:
                im_el = Image.open(raw_image_path + "test" +str(image_file_names[el]))
                #im_el = Image.open(raw_image_path + image_file_names[el])
                im_el.thumbnail(size, Image.ANTIALIAS)
                #im_el = im_el.resize(size, PIL.Image.ANTIALIAS)
                width_of_el, height_of_el = im_el.size
                old_row_width, old_row_height = img_row.size
                img_row = mergeImageHorizontally(img_row, im_el)
                new_row_width, new_row_height = img_row.size
                css_row.append((old_row_width, old_col_height, width_of_el, height_of_el))





            
        img = mergeImageVertically(img, img_row)
        css.append(css_row)
    to_return = {}
    to_return["path"] = img_name
    to_return["arr"] = arr
    img.save(static('static/image/generated/'+img_name))

    #img.save('static/image/generated/'+img_name)
    to_return["width"] , to_return["height"] = img.size
    return to_return


# generateSprite("test4.png",0)
