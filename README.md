# FirstProject_ComputerVision
Đây chính là project web hoàn chỉnh - gồm có xóa nền, đổi nền, mờ nền, làm xám nền, đăng nhập đăng ký, xem lịch sử
ĐỒ án dựa vào project này để thiết kế API


Document.
Ảnh đã được phân đoạn dựa vào mô hình - bao gồm các index nhãn - ví dụ ảnh có người thì khi di chuột vào thì chỗ người sẽ có số 15
	om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()

lấy tất cả các nhãn trong ảnh om - ma trận ảnh om

  	om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  	# testimg = decode_segmap(om)
  	# lấy tất cả các nhãn trong ảnh om (ma trận om - là ma trận đã phân đoạn và có các nhãn)
  	unique_labels = np.unique(om)
 	print("các nhãn trong ma trận om, aảnh om là: ", unique_labels)


Xóa các giá trị được chỉ định trong ma trận om
  	to_remove = [15]        # số cần xóa là 15
  	idx = np.where(np.isin(om, to_remove))
 	om[idx] = 0    # cho từ 15 thành 0 (số 0 là nền, 15 là người)

	=> om sẽ là ảnh khong phân đoạn được người nữa

	hoặc cách 2 - đang dùng

	om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
	# Xóa bớt nhãn có giá trị 8 (là cat)
	om = np.where(om == 8, 0, om) # Chuyển các giá trị bằng 8 thành 0 - số 0 (nền) sẽ được bỏ qua ở bước sau
	=> om sẽ là ảnh khong phân đoạn được cat nữa


if request.GET.get('labels_main') != None:
            labels_main = request.GET.get('labels_main')   # label main là để chọn nhãn chính và xóa nhãn còn lại
            



*** làm web
	- xuất ra các nhãn khi vừa xử lý ảnh xong (xóa nền)
	- các nhãn đó có thể click vào để làm nhân vật chính - các nhãn khác không click thì coi như là nền
	-  


def blur_background(request):
    # delete_all_image_infolder()
    labels_index_main = 0
    if request.GET.get('labels_main') != None:
        labels_index_main = int(request.GET.get('labels_main'))   # label main là để chọn nhãn chính và xóa nhãn còn lại

    uploaded_image = request.FILES.get('input_img_blur', None)
    if uploaded_image is not None:
        # lưu ảnh subject
        # uploaded_image = request.FILES['input_img_blur']
        input = Image.open(uploaded_image)
        file_name = uploaded_image.name
        input.save(path_tailen_common + file_name)
        object_BG.pathImg_blurBG.setPath(path_tailen_common + file_name)
    else:
        uploaded_image =  object_BG.pathImg_blurBG.getPath()
        input = Image.open(uploaded_image)
        # file_name = uploaded_image.name
        file_name = str(uuid.uuid4()) + '.png'
        input.save(path_tailen_common + file_name)
        object_BG.pathImg_blurBG.setPath(path_tailen_common + file_name)

    rgb, unique_labels = module_blurBG.segment(module_blurBG.dlab, path_tailen_common + file_name, labels_main=labels_index_main, show_orig=False)

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
                                            'Name_Module': 'blurBG', \
                                            'unique_labels': unique_labels})
