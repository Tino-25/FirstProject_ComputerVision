from django.db import models

# # Create your models here.
# class user(models.Model):
#     # id user
#     # tự động tăng và là khóa chính => .AutoField(primary_key=True)
#     user_id = models.AutoField(primary_key=True)
#     # tên user
#     # cho phép nhập chữ và giới hạn 50 ký tự, không được null 
#     #   => .CharField(max_length=50, null=false)
#     username = models.CharField(max_length=50, null=False)
#     # password
#     # cho phép nhập chữ và giới hạn 50 ký tự, không được null 
#     #   => .CharField(max_length=50, null=false)
#     password = models.CharField(max_length=50, null=False)
#     # email
#     # cho phép nhập chữ và giới hạn 50 ký tự, không được null 
#     #   => .CharField(max_length=50, null=false)
#     email = models.CharField(max_length=50, null=False)


#     # hàm trả về giá trị luôn có tên là __str__
#     def __str__(self):
#         return f"{self.user_id}, {self.username}, {self.password}, {self.email}"
