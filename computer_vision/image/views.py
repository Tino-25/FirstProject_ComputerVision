from django.shortcuts import render

# Create your views here.

import rembg
import uuid
from PIL import Image

from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import numpy as np
import cv2

import os
import os.path

# Apply the transformations needed
import torchvision.transforms as T

# các hàm để xóa nền ảnh
from .ModuleBG import removeBG as module_removeBG
from .ModuleBG import changeBG
from .ModuleBG import blurBG as module_blurBG
from .ModuleBG import gray_scaleBG as module_gray
from .ObjectBG import object as object_BG

# đường dẫn để lưu ảnh
path_save_removeBG = "home/static/image/removeBG/"
path_show_removeBG = "../static/image/removeBG/"
path_get_common = "home/static/image/preProcessing/"

#  chức năng thay đổi nền ảnh

path_anhnen_changeBG = "home/static/image/changeBG/imageBG/"
path_ketqua_changeBG = "home/static/image/changeBG/result/"
path_hienthiHTML_changeBG = "../static/image/changeBG/result/"
path_tailen_common = "home/static/image/preProcessing/" # là ảnh chủ thể - sẽ xóa bỏ nền để bỏ vào nền mới 

# làm mờ nền ảnh
path_ketqua_blurBG = "home/static/image/blurBG/"
path_hienthiHTML_blurBG = "../static/image/blurBG/"

# làm xám - gray nền ảnh
path_ketqua_grayBG = "home/static/image/grayBG/"
path_hienthiHTML_grayBG = "../static/image/grayBG/"


# xóa tất cả hình ảnh trong thư mục - theo đường dẫn lưu ảnh và đường dẫn lấy ảnh
def delete_all_image_infolder():
    for filename in os.listdir(path_save_removeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_save_removeBG, filename))
    for filename in os.listdir(path_get_common):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_get_common, filename))
    for filename in os.listdir(path_anhnen_changeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_anhnen_changeBG, filename))
    for filename in os.listdir(path_ketqua_changeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_ketqua_changeBG, filename))

# hàm gọi xóa tất cả hình ảnh - gọi khi remove bg
def close_all_image(request):
    delete_all_image_infolder()
    return render(request, 'removeBG.html')


# hiển thị trang chức năng xóa nền ảnh
def get_removeBG(request):
    # return render(request, 'home_result.html')
    if request.user.is_authenticated:
        username = request.user.username  # lấy tên người dùng đã đăng nhập
        return render(request, 'removeBG.html', {'Name_Module': 'removeBG', 'username': username})
    return render(request, 'removeBG.html', {'Name_Module': 'removeBG'})


# remove background lần đầu
def remove_background(request):
    delete_all_image_infolder()
    
    uploaded_image = request.FILES['image_input']
    input = Image.open(uploaded_image)
    file_name = uploaded_image.name
    input.save(path_get_common + file_name)
    object_BG.pathImg_removeBG.setPath(path_get_common + file_name)

    if request.GET.get('bg_color') != None:
        bg_color = request.GET.get('bg_color')
        bg_color = int(bg_color)
        rgb = module_removeBG.segment(module_removeBG.dlab, path_get_common + file_name, color_bg = bg_color, show_orig=False)
    else:
        rgb = module_removeBG.segment(module_removeBG.dlab, path_get_common + file_name, color_bg = 255, show_orig=False)

    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_save_removeBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    # lưu ảnh vào lịch sử
    save_img_history(request ,'removeBG', filename, brg.astype('uint8'))

    path_image_show = path_show_removeBG + filename

    return render(request, 'removeBG_result.html', {'path_image_show': path_image_show, 'Name_Module': 'removeBG'})

# remove background lần 2 - kiểu đổi nền ảnh thành đen hoặc trắng hoặc không còn nền
def remove_background_chooseBG(request):
    if request.GET.get('bg_color') != None:
        bg_color = request.GET.get('bg_color')
        bg_color = int(bg_color)
        if bg_color != 999:
            rgb = module_removeBG.segment(module_removeBG.dlab, object_BG.pathImg_removeBG.getPath(), color_bg = bg_color, show_orig=False)
            rgb_new = (rgb * 255).astype('uint8')
            brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
            filename = str(uuid.uuid4()) + '.png'
            path_image_save = path_save_removeBG + filename
            cv2.imwrite(path_image_save, brg.astype('uint8'))
            # save lịch sử
            save_img_history(request ,'removeBG', filename, brg.astype('uint8'))
        else:
            input = Image.open(str(object_BG.pathImg_removeBG.getPath()))
            output = rembg.remove(input)
            # đặt tên ảnh random
            filename = str(uuid.uuid4()) + '.png'
            path_image_save = path_save_removeBG + filename
            output.save(path_image_save)
            # save lịch sử
            name_folder = str(request.user.id)+"_"+request.user.username
            output.save("home/static/image/user_image/"+name_folder+"/removeBG/" + filename)
 
        path_image_show = path_show_removeBG + filename
    return render(request, 'removeBG_result.html', {'path_image_show': path_image_show})

#  xóa nền ảnh dùng thư viện rembg
def remove_background_rembg(request):
    # Get the uploaded image from the request
    uploaded_image = request.FILES['image_input']

    input = Image.open(uploaded_image)
    output = rembg.remove(input)

    # đặt tên ảnh random
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_save_removeBG + filename
    output.save(path_image_save)

    # lấy đường dẫn để có thể hiển thị ảnh theo path - vì path hiển thị thẻ img khác với path lưu ảnh
    path_image_show = path_show_removeBG + filename

    return render(request, 'removeBG_result.html', {'path_image_show': path_image_show})


# THAY ĐỔI NỀN HÌNH ẢNH

# gọi tới giao diện Thay đổi nền ảnh
def get_changeBG(request):
    if request.user.is_authenticated:
        username = request.user.username  # lấy tên người dùng đã đăng nhập
        return render(request, 'changeBG.html', {'Name_Module': 'changeBG', 'username': username})
    return render(request, 'changeBG.html', {'Name_Module': 'changeBG'})


# change background lần đầu
def change_background(request):
    delete_all_image_infolder()
        
    # lưu ảnh subject
    uploaded_image = request.FILES['img_subject']
    input = Image.open(uploaded_image)
    file_name = uploaded_image.name
    input.save(path_tailen_common + file_name)
    object_BG.pathImg_changeBG.setPath(path_tailen_common + file_name)

    # lưu ảnh background
    uploaded_image_bg = request.FILES['img_bg']
    input_bg = Image.open(uploaded_image_bg)
    file_name_bg = uploaded_image_bg.name
    input_bg.save(path_anhnen_changeBG + file_name_bg)
    object_BG.pathImg_changeBG.setPath(path_anhnen_changeBG + file_name_bg)

    rgb = changeBG.segment(changeBG.dlab, path_tailen_common + file_name, path_anhnen_changeBG + file_name_bg, show_orig=False)


    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_changeBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    # lưu lịch sử
    save_img_history(request ,'changeBG', filename, brg.astype('uint8'))

    path_image_show = path_hienthiHTML_changeBG + filename
    return render(request, 'changeBG.html', {'path_image_show': path_image_show, \
                                            'path_image_subject': str("../static/image/preProcessing/" + file_name), \
                                            'path_image_bg': str("../static/image/changeBG/imageBG/" + file_name_bg), \
                                            'Name_Module': 'changeBG'})
  

#  LÀM MỜ NỀN HÌNH ẢNH
# hiển thị trang chức năng làm mờ nền hình ảnh
def get_blurBG(request):
    # return render(request, 'home_result.html')
    if request.user.is_authenticated:
        username = request.user.username  # lấy tên người dùng đã đăng nhập
        return render(request, 'blurBG.html', {'Name_Module': 'blurBG', 'username': username})
    return render(request, 'blurBG.html', {'Name_Module': 'blurBG'})

def blur_background(request):
    delete_all_image_infolder()
        
    # lưu ảnh subject
    uploaded_image = request.FILES['input_img_blur']
    input = Image.open(uploaded_image)
    file_name = uploaded_image.name
    input.save(path_tailen_common + file_name)
    object_BG.pathImg_blurBG.setPath(path_tailen_common + file_name)


    rgb = module_blurBG.segment(module_blurBG.dlab, path_tailen_common + file_name, show_orig=False)


    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_blurBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    # lưu lịch sử
    save_img_history(request ,'blurBG', filename, brg.astype('uint8'))

    path_image_show = path_hienthiHTML_blurBG + filename
    return render(request, 'blurBG.html', {'path_image_show': path_image_show, \
                                            'path_image_old': str("../static/image/preProcessing/" + file_name), \
                                            'path_image_blur': str("../static/image/blurBG/" + filename), \
                                            'Name_Module': 'blurBG'})






#  LÀM Gray NỀN HÌNH ẢNH
# hiển thị trang chức năng gray nền ảnh
def get_grayBG(request):
    if request.user.is_authenticated:
        username = request.user.username  # lấy tên người dùng đã đăng nhập
        return render(request, 'gray_scaleBG.html', {'Name_Module': 'gray_scaleBG', 'username': username})
    return render(request, 'gray_scaleBG.html', {'Name_Module': 'gray_scaleBG'})

def gray_background(request):
    delete_all_image_infolder()
        
    # lưu ảnh subject
    uploaded_image = request.FILES['input_img_gray']
    input = Image.open(uploaded_image)
    file_name = uploaded_image.name
    input.save(path_tailen_common + file_name)
    object_BG.pathImg_grayBG.setPath(path_tailen_common + file_name)


    rgb = module_gray.segment(module_gray.dlab, path_tailen_common + file_name, show_orig=False)


    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_grayBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))
    
    # lưu lịch sử
    save_img_history(request ,'grayBG', filename, brg.astype('uint8'))

    path_image_show = path_hienthiHTML_grayBG + filename
    return render(request, 'gray_scaleBG.html', {'path_image_show': path_image_show, \
                                            'path_image_old': str("../static/image/preProcessing/" + file_name), \
                                            'path_image_gray': str("../static/image/grayBG/" + filename), \
                                            'Name_Module': 'grayBG'})




# cách dùng hàm này - ví dụ:  save_img_history(request ,'removeBG', filename, brg.astype('uint8'))
def save_img_history(request, tool, filename, img):
    name_folder = str(request.user.id)+"_"+request.user.username
    cv2.imwrite("home/static/image/user_image/"+name_folder+"/"+str(tool)+"/" + filename, img.astype('uint8'))

