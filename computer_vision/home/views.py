from django.shortcuts import render
# 2 dòng dưới tắt hiển thị lỗi -> phiên bản models sẽ đổi mới
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Create your views here.
def get_home(request):
    # return render(request, 'home_result.html')
    if request.user.is_authenticated:
        username = request.user.username  # lấy tên người dùng đã đăng nhập
        return render(request, 'home.html', {'username': username})
    return render(request, 'home.html')
