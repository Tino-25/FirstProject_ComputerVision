from torchvision import models
# 2 dòng dưới => để không hiển thị lỗi ở console - có hiển thị lỗi nhwung vẫn chạy
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import torch
# 2 lệnh dưới để kiểm tra có cuda không - nếu không thì set device là cpu thay vì cuda
# torch.cuda.is_available = lambda : False
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import numpy as np
import cv2
# Apply the transformations needed
import torchvision.transforms as T
# import chardet

from . import common


# Define the helper function
def decode_segmap(image, source, nc=21):
    # label_colors = np.array([(0, 0, 0),  # 0=background
    #                          # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
    #                          (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
    #                          # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
    #                          (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
    #                          # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
    #                          (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
    #                          # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
    #                          (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])
    # đổi thành cùng như vậy là vì khi thử nghiệm thì thấy như vậy mới hiện rõ được đối tượng
    label_colors = np.array([(0, 0, 0),  # 0=background
                            (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), 
                            (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), 
                            (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), 
                            (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), (192, 128, 128), ])


    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]

    rgb = np.stack([r, g, b], axis=2)

    # Load the foreground input image
    foreground = cv2.imread(source)

    # Change the color of foreground image to RGB
    # and resize image to match shape of R-band in RGB output map
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB)
    foreground = cv2.resize(foreground, (r.shape[1], r.shape[0]))

    # Create a Gaussian blur of kernel size 7 for the background image
    blurredImage = cv2.GaussianBlur(foreground, (7, 7), 0)

    # Convert uint8 to float
    foreground = foreground.astype(float)
    blurredImage = blurredImage.astype(float)

    # Create a binary mask of the RGB output map using the threshold value 0
    th, alpha = cv2.threshold(np.array(rgb), 0, 255, cv2.THRESH_BINARY)

    # Apply a slight blur to the mask to soften edges
    alpha = cv2.GaussianBlur(alpha, (7, 7), 0)

    # Normalize the alpha mask to keep intensity between 0 and 1
    alpha = alpha.astype(float) / 255

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - alpha, blurredImage)

    # Add the masked foreground and background
    outImage = cv2.add(foreground, background)

    # Return a normalized output image for display
    return outImage / 255


def segment(net, path, show_orig=True, labels_main = 0, dev='cpu'):
    img = Image.open(path)

    if show_orig: plt.imshow(img); plt.axis('off'); plt.show()
    # Comment the Resize and CenterCrop for better inference results
    trf = T.Compose([T.Resize(450),
                     # T.CenterCrop(224),
                     T.ToTensor(),
                     T.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])
    inp = trf(img).unsqueeze(0).to(dev)
    out = net.to(dev)(inp)['out']
    om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()


    # nhận tất cả các nhãn trong ảnh đã phân đoạn
    unique_labels_index = np.unique(om)
    unique_labels_index=np.delete(unique_labels_index, np.where(unique_labels_index == 0))   # xóa só 0 trong unique_labels_index
    print("các nhãn trong ma trận om, ảnh om là: ", unique_labels_index)
    unique_labels = common.get_labels_from_index(unique_labels_index)

    print("labels_main nhận được là: ",labels_main)
    # Xóa bớt nhãn có giá trị 8 (là cat)
    # to_remove = [8, 3]        # số cần xóa là 8 và 3
    if labels_main!=0:   # vì labels_main mặc định = 0 và nếu có truyền vào thì sẽ thực hiện
        to_remove = common.no_get_only_index(unique_labels_index, labels_main)   # không lấy index = labels_main - để xóa các index còn lại
        idx = np.where(np.isin(om, to_remove))
        om[idx] = 0


    rgb = decode_segmap(om, path)
    print(zip(unique_labels_index, unique_labels))
    # plt.imshow(rgb);
    # plt.axis('off');
    # plt.show()
    return rgb, zip(unique_labels_index, unique_labels)


# sử dụng thư viện PyTorch để tải một mô hình phân đoạn (segmentation) đã được huấn luyện sẵn,
#                   đó là Deeplabv3 ResNet101, và đặt mô hình vào chế độ đánh giá (evaluation mode).
# models.segmentation.deeplabv3_resnet101: Gọi hàm để tạo một mô hình Deeplabv3 ResNet101 cho phân đoạn ảnh.
#                   Gọi hàm để tạo một mô hình Deeplabv3 ResNet101 cho phân đoạn ảnh.
#                   pretrained=1: Tham số pretrained cho biết rằng ta muốn tải trọng số đã được huấn luyện sẵn của mô hình.
#                   Nếu pretrained=0, mô hình sẽ được khởi tạo ngẫu nhiên và chưa được huấn luyện.
# .eval(): Chuyển mô hình sang chế độ đánh giá (evaluation mode), có nghĩa là mô hình không được huấn luyện thêm
#          và các layer trong mô hình không được cập nhật các trọng số khi tính toán đầu ra.
dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()




# #  hiển thị ảnh
# fig = plt.figure(figsize=(16, 9)) # Tạo vùng vẽ tỷ lệ 16:9
# (ax1, ax2), (ax3, ax4) = fig.subplots(2, 2) # Tạo 2 vùng vẽ con

# # Đọc và hiển thị ảnh gốc
# # ảnh girl
# ax1.imshow(girl_goc, cmap='gray')
# ax1.set_title("ảnh gốc")
# ax2.imshow(girl_blur_bacground, cmap='gray')
# ax2.set_title("ảnh làm mờ nền")
# # ảnh boy
# ax3.imshow(boy_goc, cmap='gray')
# ax3.set_title("ảnh gốc")
# ax4.imshow(boy_blur_bacground, cmap='gray')
# ax4.set_title("ảnh làm mờ nền")
# plt.show()