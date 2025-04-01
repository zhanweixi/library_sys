from commons.mixins.models import CommonModelMixin
from django.db import models


# Create your models here.


class LibraryUser(CommonModelMixin):
    type_choices = (
        (0, "读者"),
        (1, "管理人员")
    )
    sex_choices = (
        (0, "男"),
        (1, "女")
    )
    name = models.CharField(max_length=50, verbose_name="姓名")
    code = models.CharField(max_length=50, unique=True, verbose_name="编号")
    sex = models.CharField(max_length=5, blank=True, choices=sex_choices, verbose_name="性别")
    phone = models.CharField(max_length=50, verbose_name="电话")
    email = models.EmailField(blank=True, verbose_name="电子邮件")
    type = models.CharField(max_length=5, blank=True, choices=type_choices, verbose_name="用户类型")

    class Meta():
        db_table = "library_user"
        verbose_name = "图书用户登记表"
        verbose_name_plural = verbose_name


class BooksModel(CommonModelMixin):
    ISBN = models.CharField(max_length=50, blank=False, unique=True, verbose_name="图书编号")
    name = models.CharField(max_length=50, verbose_name="图书名称")
    type = models.CharField(max_length=50, verbose_name="图书类型")
    author = models.CharField(max_length=50, verbose_name="作者")
    publish = models.CharField(max_length=50, verbose_name="出版社")
    publish_date = models.DateTimeField(verbose_name="出版日期")
    numbers = models.CharField(max_length=50, verbose_name="书籍数量")
    intro = models.TextField(verbose_name="图书简介")

    class Meta():
        db_table = "books_table"
        verbose_name = "图书管理表"
        verbose_name_plural = verbose_name


class BorrowModel(CommonModelMixin):
    state_choices = (
        (0, "借阅仲"),
        (1, "已归还"),
    )
    reader_id = models.CharField(max_length=50, verbose_name="读者编号")
    book_id = models.CharField(max_length=50, verbose_name="图书编号")
    state = models.CharField(max_length=5, default=0, choices=state_choices, verbose_name="借阅状态")
    getDate = models.DateTimeField(verbose_name="借阅时间")
    retDate = models.DateTimeField(null=True, verbose_name="归还时间")
    max_getDate = models.DateTimeField(verbose_name="最大借阅时间")

    class Meta():
        db_table = "borrow_db"
        verbose_name = "借阅表"
        verbose_name_plural = verbose_name
