from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout    # dùng để đăng nhập, đăng xuất
# from .models import user as userModel
from django.contrib.auth.models import User as userModel   # là bảng user tạo sẵn của django - bảng này có sẵn


# Create your views here.
def get_login(request):
    # select dữ liệu từ bảng user
    if request.method == 'GET':
        register_ok = request.GET.get('ok')    # phản hồi khi đã đăng ký xong
        return render(request, 'login.html', {'register_ok': register_ok}) 
    user_list = userModel.objects.filter().order_by('user_id')
    return render(request, 'login.html', {'user_list' : user_list})

# register
def add_user(request):
    # lấy thông tin từ form
    if request.method == 'POST':
        # lấy dữ liệu từ post
        username = request.POST['name_register']
        email = request.POST['email_register']
        password = request.POST['password_register']
        # tiến hành save
        user = userModel.objects.create_user(
            username = username,
            email = email,
            password = password
        )
        # dùng .create_user() sẽ tự động lưu vào csdl luôn - mk cũng sẽ được mã hóa luôn
      

        # return render(request, 'login.html', {'ok' : 'ok'})
        return redirect('/login?ok=ok')
    else:
        # tự tạo file error.html (Templates/error.html)
        return render(request, 'error.html')

# login
def login_user(request):
    # Kiểm tra nếu người dùng đã đăng nhập thì chuyển hướng đến trang chủ
    if request.user.is_authenticated:
        return redirect('/?login_ok=ok')

    # Xử lý form đăng nhập khi được submit
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kiểm tra tên đăng nhập và mật khẩu
        user = authenticate(request, username=username, password=password)
        print("Đây là user đã login: ",user)
        if user is not None:
            # Nếu tên đăng nhập và mật khẩu đúng, đăng nhập và chuyển hướng đến trang chủ
            login(request, user)
            # tạo các folder để lưu lịch sử chỉnh sửa
            create_folder_user(request.user.id, request.user.username)
            return redirect('/')
        else:
            # Nếu tên đăng nhập hoặc mật khẩu không đúng, hiển thị thông báo lỗi
            error_message = "Tên đăng nhập hoặc mật khẩu không đúng"
            return render(request, 'login.html', {'error_message': error_message})

    # Nếu không phải là method POST, hiển thị form đăng nhập
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


import os
# tạo folder với tên là id_username
# tạo thêm 4 folder tương ứng 4 chức năng để lưu lịch sử
def create_folder_user(id, username):
    name_folder = str(id)+"_"+username
    new_folder_user_path = "home/static/image/user_image/"+name_folder
    # Kiểm tra xem thư mục đã tồn tại hay chưa
    if not os.path.exists(new_folder_user_path):
        # Nếu chưa tồn tại, sử dụng hàm mkdir để tạo thư mục mới
        os.mkdir(new_folder_user_path)
        new_folder_removeBG_path = "home/static/image/user_image/"+name_folder+"/removeBG"
        new_folder_changeBG_path = "home/static/image/user_image/"+name_folder+"/changeBG"
        new_folder_blurBG_path = "home/static/image/user_image/"+name_folder+"/blurBG"
        new_folder_grayBG_path = "home/static/image/user_image/"+name_folder+"/grayBG"
        os.mkdir(new_folder_removeBG_path)
        os.mkdir(new_folder_changeBG_path)
        os.mkdir(new_folder_blurBG_path)
        os.mkdir(new_folder_grayBG_path)
    else:
        print("Thư mục đã tồn tại!")


    
