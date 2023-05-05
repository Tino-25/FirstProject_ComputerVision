 # định nghĩa class để lưu đường dẫn file ảnh
# 1: là để chuyển background từ đen sang trắng rồi từ trắng sang đen
class PathImage:
    def __init__(self, PathImage=''):
        self.PathImage = PathImage
    def getPath(self):
        return self.PathImage
    def setPath(self, path):
        self.PathImage = path

pathImg_removeBG = PathImage()
pathImg_changeBG = PathImage()
pathImg_blurBG = PathImage()
pathImg_grayBG = PathImage()