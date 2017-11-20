from django.shortcuts import render
from . import generate_sprite as gs
from . import generate_sprite2
from django.http import HttpResponse,JsonResponse
import json
import random
import time
import string
from flask import Markup
from django.conf import settings
import os
from .models import CssConf
from django.shortcuts import render_to_response
static_server_loc = settings.STATIC_SERVER_LOC
mat_i1 = 14
mat_j1 = 14

image_map = {}
resize_height = 22
resize_width = 9

hwref = {"0" : {"height" : resize_height , "width" : resize_width },"1" : {"height" : resize_height , "width" : resize_width },"2" : {"height" : resize_height , "width" : resize_width },"3" : {"height" : resize_height , "width" : resize_width },"4" : {"height" : resize_height , "width" : resize_width },"5" : {"height" : resize_height , "width" : resize_width },"6" : {"height" : resize_height , "width" : resize_width },"7" : {"height" : resize_height , "width" : resize_width },"8" : {"height" : resize_height , "width" : resize_width },"9" : {"height" : resize_height , "width" : resize_width }, "10" : {"height" : resize_height , "width" : 5 } , "11" : {"height" : resize_height , "width" : resize_width },"12" : {"height" : resize_height , "width" : 4 },"13" : {"height" : resize_height , "width" : 5 }}

image_data = {}
image_map = {}
# Create your views here.=


def index(request):
    return render_to_response('index.html')

def generate_new_sprites(request):
    global image_map,image_data 
    for i in range(10):
        returnval = generate_sprite2.generateSprite("type0_"+str(i)+".png",0)
        image_map["type0_"+str(i)] = returnval

    # generate type1 image
    for i in range(10):
        returnval = generate_sprite2.generateSprite("type1_" + str(i)+".png", 1)
        image_map["type1_" + str(i)] = returnval

    # generate type2 image
    for i in range(10):
        returnval = generate_sprite2.generateSprite("type2_" + str(i)+".png", 2)
        image_map["type2_" + str(i)] = returnval

    # generate type3 image
    for i in range(10):
        returnval = generate_sprite2.generateSprite("type3_" + str(i)+".png", 3)
        image_map["type3_" + str(i)] = returnval

    #with open('data.txt', 'w') as outfile:
    #    json.dump(image_map, outfile)
    #    outfile.close()
    for x in range(100):
        css,arr,img_name = gs.generateSprite('sprite'+str(x) +'.png')
        image_data[img_name] = (css,arr)
    return HttpResponse("successfully iniitialized")



def masknumber(request): 
    phone = request.GET.get('phone')
    image_file = None
    file_name = None
    logic_type = random.randint(0, 1)
    
    if(logic_type == 0):
        return phoneMask2(phone)

    if phone is not None:
        file_name = random.choice(list(image_data.keys()))
        #image_file = 'image/'+file_name+"?"+str(int(time.time()))
        image_file = file_name
    identf = 'nmbrIcon'+''.join(random.choice(string.ascii_lowercase) for x in range(3))
    css_classes,mark_up = createMarkUp(phone,identf)
    css_style = createStyle(identf,css_classes, file_name,image_file, phone)
    d = {}
    d['markup'] = mark_up
    print(d['markup'])
    d['css'] = css_style
    return JsonResponse(d) 


def phoneMask2(phone):
    image_file = None
    file_name = None
    css_positions = []
    image_file = None
    if phone is not None:
        # generateSprite("8950317605")
        css_positions , image_file , image_file1 = generateCssPositions(phone)
        #image_file = image_dict[phone][1]
        # image_file = 'image/' + "8950317605.png" + "?" + str(int(time.time()))
        # image_file1 = 'image/' + "8950317605_1.png" + "?" + str(int(time.time()))
        identf = 'nmbrIcon'+''.join(random.choice(string.ascii_lowercase) for x in range(3))
        image_file = image_file
        image_file1 = image_file1

        html_tags, mark_up = createMarkUp2(phone,identf)

        css_style = createStyle2(identf ,html_tags, css_positions, image_file,image_file1)
        d = {}
        d['markup'] = mark_up
        d['css'] = css_style
        return JsonResponse(d)

def createMarkUp2(phone,identf):
    html = []
    css_classes = []
    for c in phone:
        if(c == '-'):
            c = "10"
        elif(c == '+'):
            c = "11"
        elif(c == ','):
            c = "12"
        elif(c == ' '):
            c = "13"
        #print(c)
        obj = {"num" : c}
        css_class = ''.join(random.choice(string.ascii_letters) for x in range(3))
        css_class = identf+"-" + css_class
        obj["css_class"] = css_class
        css_classes.append(obj)
        html.append('<span class="' + css_class + '">' + '</span>')

    return (css_classes, Markup('<div class="nmbr">' + "".join(html) + '</div>'))

def createMarkUp(phone,identf):
    html = []
    css_classes = []
    for c in phone:
        css_class = ''.join(random.choice(string.ascii_lowercase) for x in range(3))
        css_class = identf + "-"+css_class
        css_classes.append(css_class)
        html.append('<span class="'+css_class+'">' +'</span>')
    
    return (css_classes, Markup('<div class="nmbr">'+ "".join(html) +'</div>'))

def createStyle2(identf ,css_classes, css_positions, image_name,image_name1):
    global image_map,image_data
    shuffled = [a for a in css_classes]
    random.shuffle(shuffled)
    # css = '.nmbr span{float: left !important;}\n' + \
    #       '[class^="nmbrIcon-"] { background-image: url(' + image_name + '),url(' + image_name1 + ');background-repeat: no-repeat; vertical-align:middle;height: 48px; width:48px;display:inline-block; }'
    i = 0
    url_image = os.path.join(static_server_loc ,'static/css_sprites/image/generated/'+image_name)
    url_image1 = os.path.join(static_server_loc , 'static/css_sprites/image/generated/'+image_name1)
    css = '.nmbr span{}\n' + \
           '[class^="'+identf+'-"] { background-image: url(' + url_image  + '),url(' + url_image1 + ');background-repeat: no-repeat; vertical-align:middle;display:inline-block; }'
    # css = ''
    for a in css_classes:
        # index = css_classes.index(a)
        posy = css_positions[i][0] * -1
        posx = css_positions[i][1] * -1
        num = a["num"]
        height = str(hwref[num]["height"])
        width = str(hwref[num]["width"])
        c = ' .' + a["css_class"] + '{ background-position : ' + str(posx) + 'px ' + str(posy) + 'px; height: '+str(height)+'px; width:'+str(width)+'px; }'

        css = css + '\n' + c
        i = i+ 1

    return Markup(css)


def generateCssPositions(phone):
    global image_map,image_data
    positions = []
    image_type = random.randrange(0, 3, 2)
    # image_type = 0
    image_no1 = "type"+str(image_type) +"_" +str(random.randint(0, 9))
    image_no2 = "type"+str(image_type + 1) +"_" +str(random.randint(0, 9))
    image_height = image_map[image_no1]["height"]
    image_width = image_map[image_no1]["width"]
    print(phone)
    for c in phone:
        # pick random row for each digit
        print(str(c))
        if(image_type == 0):
            image_number = random.randint(0, 1)
            if (image_number == 0):
                row = random.randrange(1, 2 * mat_i1, 2)
                arr = image_map[image_no1]["arr"]
            else:
                row = random.randrange(0, 2 * mat_i1, 2)
                arr = image_map[image_no2]["arr"]
            try:
                if(c == '-'):
                    num_ip = 10
                elif(c == '+'):
                    num_ip = 11
                elif(c == ','):
                    num_ip = 12
                elif(c == ' '):
                    num_ip = 13
                else:
                    num_ip = int(c)
                #print(str(arr[row].index(num_ip)))
                #print(str(num_ip))
                positions.append((row, arr[row].index(num_ip)))
            except:
                raise ValueError(str(arr[row]))
        else:
            image_number = random.randint(0, 1)
            if (image_number == 0):
                col = random.randrange(1, 2 * mat_j1, 2)
                arr = image_map[image_no1]["arr"]
            else:
                col = random.randrange(0, 2 * mat_j1, 2)
                arr = image_map[image_no2]["arr"]
            try:
                col_arr = [row[col] for row in arr]
                if(c == '-'):
                    num_ip = 10
                elif(c == '+'):
                    num_ip = 11
                elif(c == ','):
                    num_ip = 12
                elif(c == ' '):
                    num_ip = 13
                else:
                    num_ip = int(c)
                #print(str(col_arr.index(num_ip)))
                #print(str(num_ip))
                positions.append((col_arr.index(num_ip),col))
                #positions.append((row, arr[row].tolist().index(int(c))))
            except:
                raise ValueError(str(arr[row]))



    if(image_type == 0):
        css = [((x[0]) * (float(image_height) / (2 * mat_i1)), (x[1]) * (float(image_width) / mat_j1)) for x in positions]
    else:
        css = [((x[0]) * (float(image_height) / mat_i1), (x[1]) * (float(image_width) /( 2 * mat_j1))) for x in positions]


    return (css , image_map[image_no1]["path"]+"?"+str(int(time.time())),image_map[image_no2]["path"]+"?"+str(int(time.time())))

def createStyle(identf,css_classes, file_name,image_name, phone):
    global image_map,image_data
    css_all, arr = image_data[file_name]
    
    #css = '.nmbr span{float: left !important; margin-right: 1px;}\n' + \
    #    '[class^="nmbrIcon-"] { background-image: url('+image_name+');background-repeat: no-repeat; vertical-align:middle;display:inline-block; }'
    url_image = os.path.join(static_server_loc,'static/css_sprites/image/generated/'+image_name)
    css = '.nmbr span{}\n' + \
        '[class^="'+identf+'-"] { background-image: url('+url_image+');background-repeat: no-repeat; vertical-align:middle;display:inline-block; }'
    
    randomized_css = []
    for c in phone:
        if(c == '-'):
            tnum = 10
        elif(c== '+'):
            tnum = 11
        elif(c== ','):
            tnum = 12
        elif(c== ' '):
            tnum = 13
        else:
            tnum = int(c)
        row = random.randint(0, 9)
        css_rnd = css_all[row]
        randomized_css.append(css_rnd[arr[row].tolist().index(tnum)])
    
    previous_width_diff = '0px'
    previous_rotation = 90
    for a in css_classes:
        index = css_classes.index(a)
        css_dict = {}
        background_position = str(randomized_css[index][0]*-1)+'px ' + str(randomized_css[index][1]*-1)+'px'
        css_dict['background-position'] = background_position
        width,height = (randomized_css[index][2],randomized_css[index][3]) if randomized_css[index][4] not in (90,270)\
            else (randomized_css[index][3],randomized_css[index][2])
        css_dict['width'] = str(width)+'px'
        css_dict['height'] = str(height)+'px'
        css_dict['transform'] = 'rotate('+str(randomized_css[index][4])+'deg)'
        css_dict['padding-top'] = '0px' if randomized_css[index][4] not in (90,270) else str(randomized_css[index][3]-randomized_css[index][2])+'px'
        css_dict['margin-left'] = previous_width_diff if randomized_css[index][4] not in (180,360) else '0px'
        previous_width_diff = '0px' if randomized_css[index][4] not in (90,270) else str(randomized_css[index][2]-randomized_css[index][3])+'px'
        c = ' .' +a+'{'+';'.join([b+':'+css_dict[b] for b in css_dict.keys()])+'}'
        css = css + '\n' + c
        
    return Markup(css)
