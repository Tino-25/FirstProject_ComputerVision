from torchvision import models
from PIL import Image
import torch
import numpy as np
import cv2

from . import common


# Apply the transformations needed
import torchvision.transforms as T


# Define the helper function
def decode_segmap(image, source, color_bg = 255, nc=21):
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

    # thay đổi máu sắc trong ảnh đầu vào theo nhãn tương ứng
    for l in range(0, nc):
        idx = image == l    #idx = True tương ứng với vị trí của các pixel có nhãn bằng với giá trị nhãn đang xét
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
        # r[True]: thí sẽ được xử lý - cho bằng với giá trị tương ứng với nhãn
        # r[False]: thì sẽ bị bỏ qua - tức là sẽ = 0 như thiết lập ở trên

    rgb = np.stack([r, g, b], axis=2)    # tạo ma trận anh rgb - mỗi pxx là một vector [r, g, b]

    # Load the foreground input image - tải hình ảnh đầu vào (tiền cảnh)
    foreground = cv2.imread(source)

    # Change the color of foreground image to RGB - thay đổi màu của tiền cảnh thành RGB
    # and resize image to match shape of R-band in RGB output map - thay đổi kích thước ảnh vào bằng với ảnh r (coi như là bằng kích thước của ảnh đã phân đoạn bằng model)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB)
    foreground = cv2.resize(foreground, (r.shape[1], r.shape[0]))

    # Tạo nền là các px có giá trị color_bg (color_bg = 255 thì nền trắng, = 0 thì nền đen)
    # with the same size as RGB output map - có cùng kích thước RGB đầu ra
    background = color_bg * np.ones_like(rgb).astype(np.uint8)

    # Convert uint8 to float - chuyển đổi unit8 thnafh float
    foreground = foreground.astype(float)
    background = background.astype(float)

    # Create a binary mask of the RGB output map using the threshold value 0
    # Tạo mặt nạ nhị phân của bản đồ đầu ra RGB bằng giá trị ngưỡng 0 (ra 1 ma trận o và 1 với ngưỡng là 0)
    # th là ngưỡng đã sử dụng: 0
    # alpha là ảnh đã được cắt ngưỡng
    th, alpha = cv2.threshold(np.array(rgb), 0, 255, cv2.THRESH_BINARY)

    # Apply a slight blur to the mask to soften edges
    # áp dụng một chút làm mờ cho mặt nạ đẻ làm mềm cạnh
    alpha = cv2.GaussianBlur(alpha, (7, 7), 0)

    # Normalize the alpha mask to keep intensity between 0 and 1
    # Bình thường hóa mặt nạ alpha để giữ cường độ từ 0 đến 1
    # muốn chia phải .astype(float)
    alpha = alpha.astype(float) / 255

    # Multiply the foreground with the alpha matte
    # nhân tiền cảnh (ảnh vào đã xử lý ở trên) với ảnh alpha ở trên
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    # nhân nền với 1 - alpha
    background = cv2.multiply(1.0 - alpha, background)

    # Add the masked foreground and background
    outImage = cv2.add(foreground, background)

    # Return a normalized output image for display - trả về đầu ra được chuẩn hóa để hiển thị
    return outImage / 255



def segment(net, path, color_bg = 255, labels_main = 0, show_orig=True):
    dev='cpu'
    #img = Image.open(path)   nếu có ảnh (RGBA thì sẽ là ảnh 4 kênh thì bị lỗi
    # nên phải dùng dòng dưới để chuyển tất cả ảnh vào thành ảnh 3 kênh RGB)
    img = Image.open(path).convert('RGB')
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

    rgb = decode_segmap(om, path, color_bg, 21)

    return rgb, zip(unique_labels_index, unique_labels)
    # plt.imshow(rgb)
    # plt.axis('off')
    # plt.show()

dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()