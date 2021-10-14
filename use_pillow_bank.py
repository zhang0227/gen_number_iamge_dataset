#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   use_pillow_bank.py
@Time    :   2021/10/13 10:51:35
@Author  :   zhangxl 
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import glob



# 用来随机生成一个字符串
def gene_text():
    source = list(string.digits)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))

# # 用来绘制干扰线
# def gene_line(draw, width, height):
#     begin = (random.randint(0, width), random.randint(0, height))
#     end = (random.randint(0, width), random.randint(0, height))
#     draw.line([begin, end], fill=linecolor)

# 生成卡号
def gene_code(number, space_number):

    text = gene_text()  # 生成字符串
    index_list = random.sample(range(1, number), space_number)
    index_list.append(0)
    index_list.sort()
    full_text = ""
    for i in range(space_number):
        full_text = full_text + text[index_list[i]:index_list[i+1]] + " "
    full_text = full_text + text[index_list[space_number]:]
    full_number = number + space_number
    return full_text, full_number

# 画图
def draw_image(full_text, full_number, font_path,fontcolor, save_path,index,background_path=None,background_color = (200,200,200)):
    
    width_dict = {"CENTURY.TTF":0,"bankcard1.ttf":5,"simsun.ttc":0, "seguihis.ttf":0,}
    height_dict = {"CENTURY.TTF":12,"bankcard1.ttf":0,"simsun.ttc":9, "seguihis.ttf":16,}
    
    
    font = ImageFont.truetype(font_path, 50)
    font_width, font_height = font.getsize(full_text)

    width, height = font_width + (full_number*width_dict[os.path.basename(font_path)]) + 5 , font_height-height_dict[os.path.basename(font_path)]
    if background_path != None:
        image = Image.open(background_path)
        #print(background_path,len(image.split()))
        
        w, h = image.size

        crop_x_max = w - width
        crop_y_max = h - height
        
        if crop_x_max < 0 or crop_y_max < 0 or len(image.split()) !=3:
            
            background = tuple(random.sample(range(0,255),3))
            image = Image.new('RGBA',(width,height),background) #创建图片
        else:
            start_crop_x = random.randint(0, crop_x_max)
            start_crop_y = random.randint(0, crop_y_max)
            end_crop_x = start_crop_x + width
            end_crop_y = start_crop_y + height

            crop_box = (start_crop_x, start_crop_y, end_crop_x, end_crop_y)
            image = image.crop(crop_box)
    else:
        image = Image.new('RGBA',(width,height),background_color) #创建图片

    draw = ImageDraw.Draw(image)  # 创建画笔

    x, y = (width - font_width) / \
        full_number, ((height - font_height) / full_number)-height_dict[os.path.basename(font_path)]
    
    for idx, char in enumerate(full_text):
        #print(fontcolor)
        draw.text((x, y), char, font=font, fill=fontcolor)
        char_w, char_h = draw.textsize(char, font)
        x = x + char_w + width_dict[os.path.basename(font_path)]
        y = y

    text = full_text.replace(" ","")
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强

    image.save(os.path.join(save_path, index+'.png'))  # 保存图片
    with open(os.path.join(save_path, index+'.txt'),"w") as f :
        f.write(text)
    f.close()
    del draw

def get_filename(path):

    filename = os.path.basename(path).split(".")[0]
    return filename


if __name__ == "__main__":

    # 生成样本数量
    num = 5000
    start_num = 15000
    all_random = True
    font_path = "./font/"
    font_list = []
    font_types = ('*.ttf', '*.TTF', '*.ttc')
    for font_type in font_types:
        font_list.extend(glob.glob(os.path.join(font_path,font_type)))
    
    background_path = "./background/"
    background_list = []
    image_types = ('*.jpg', '*.jpeg', '*.png')
    for image_type in image_types:
        background_list.extend(glob.glob(os.path.join(background_path,image_type)))
    

    
    if all_random:

        save_path = "./all_random"
        
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        
        for i in range(num):

            # 生成几位数的号码
            number = random.randint(16,19)
            # 生成几个空格
            space_number = random.randint(0,4)
            # 随机字体颜色
            fontcolor = tuple(random.sample(range(0,255),3))

            #随机背景
            back_index = random.randint(0,len(background_list)-1)
            background_file = background_list[back_index]
            #随机字体
            font_index = random.randint(0,len(font_list)-1)
            font_file = font_list[font_index]
            #font_file = "./font/seguihis.ttf"#"simsun.ttc" "seguihis.ttf"

            full_text, full_number = gene_code(number, space_number)
            
            index = str(i+start_num).zfill(6)
            
            draw_image(full_text, full_number, font_file, fontcolor,save_path,index,background_file)
            print(index)
    else:

        # # # 生成几位数的号码
        # number = 16
        # # 生成几个空格
        # space_number = 3
        
        fontcolor = (192,192,192)#银色
        save_path = "./font_192_back_rand"
        for i in range(num):

            # 生成几位数的号码
            number = random.randint(16,19)
            # 生成几个空格
            space_number = random.randint(0,4)

            full_text, full_number = gene_code(number, space_number)
            
            # 字体颜色，默认为蓝色
            #fontcolor = (192,192,192)#银色
        
            #随机背景
            back_index = random.randint(0,len(background_list)-1)
            background_file = background_list[back_index]
            
            #随机字体
            font_index = random.randint(0,len(font_list)-1)
            font_file = font_list[font_index]

            #save_path = get_filename(font_file)+ '-' + get_filename(background_file) + '-' + str(number) + '-' + str(space_number)
            
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            
            index = str(i+start_num).zfill(6)
            
            draw_image(full_text, full_number, font_file,fontcolor, save_path,index,background_file)
            print(index)
