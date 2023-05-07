
labels_text = ["background", 
                "aeroplane", "bicycle", "bird", "boat", "bottle",
                "bus", "car", "cat", "chair", "cow",
                "dining table", "dog", "horse", "motorbike", "person",
                "potted plant", "sheep", "sofa", "train", "tv/monitor"]

# List_index là một mảng các index
# lấy ten của nhãn dựa vào mảng index được truyền vào
def get_labels_from_index(List_index):
    list_labels = []
    for i in List_index:
        if i == 0:
            continue
        list_labels.append(labels_text[i])
    return list_labels


# là chỉ lấy index này và xóa các index còn lại trong list
def no_get_only_index(list_index, index):
    list_return = []
    for i in list_index:
        if i == index:
            continue
        list_return.append(i)
    return list_return