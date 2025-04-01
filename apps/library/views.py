import datetime

from apps.library.models import BorrowModel, BooksModel
from commons.common import celery_logger
from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

logger = celery_logger


class LibraryView(APIView):
    """图书相关信息管理"""

    def get(self, request):
        """查询图书信息"""
        try:
            ISBN = request.GET.get("ISBN")
            name = request.GET.get("name")
            type = request.GET.get("type")
            author = request.GET.get("author")
            # 添加筛选条件
            q_obj = Q()
            if ISBN:
                q_obj &= Q(ISBN=ISBN)
            if name:
                q_obj &= Q(name=name)
            if type:
                q_obj &= Q(type=type)
            if author:
                q_obj &= Q(author=author)
            # 查询数据数据
            rdata = list()
            queryset = BooksModel.objects.filter(q_obj)
            for obj_ in queryset:
                rdata.append(model_to_dict(obj_))
            result = {"code": 0, "status": "success", "message": "", "data": rdata}
        except Exception as e:
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)

    @transaction.atomic
    def put(self, request):
        """录入图书信息"""
        save_id = transaction.savepoint()
        try:
            rdata = request.data
            BooksModel.objects.create(**rdata)
            transaction.savepoint_commit(save_id)
            result = {"code": 0, "status": "success", "message": "", "data": []}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)

    @transaction.atomic
    def post(self, request):
        """修改图书信息"""
        save_id = transaction.savepoint()
        try:
            rdata = request.data
            ISBN = rdata.get("ISBN")
            if ISBN:
                obj_ = BooksModel.objects.filter(ISBN=ISBN)
                obj_.update(**rdata)
                transaction.savepoint_commit(save_id)
            else:
                raise EOFError("参数没有图书编码ISBN")
            result = {"code": 0, "status": "success", "message": "", "data": []}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)

    @transaction.atomic
    def delete(self, request):
        """销毁图书信息"""
        save_id = transaction.savepoint()
        try:
            rdata = request.data
            ISBN = rdata.get("ISBN")
            if ISBN:
                BooksModel.objects.filter(ISBN=ISBN).delete()
                transaction.savepoint_commit(save_id)
            else:
                raise EOFError("参数没有图书编码ISBN")
            result = {"code": 0, "status": "success", "message": "", "data": []}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)


class BorrowView(APIView):
    """读者借阅图书和归还图书API"""

    @transaction.atomic
    def put(self, request):
        """读者借阅图书"""
        save_id = transaction.savepoint()
        try:
            rdata = request.data
            book_id = rdata.get("book_id")
            reader_id = rdata.get("reader_id")
            if book_id and reader_id:
                now_time = datetime.datetime.now()
                rdata["state"] = 0
                rdata["getDate"] = now_time
                rdata["max_getDate"] = now_time + datetime.timedelta(days=30)
                BorrowModel.objects.create(**rdata)
                transaction.savepoint_commit(save_id)
            else:
                raise EOFError("没有传递图书编号或者读者编号")
            result = {"code": 0, "status": "success", "message": "", "data": []}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)

    @transaction.atomic
    def post(self, request):
        """读者归还图书"""
        save_id = transaction.savepoint()
        try:
            rdata = request.data
            book_id = rdata.get("book_id")
            reader_id = rdata.get("reader_id")
            if reader_id and reader_id:
                rdata['state'] = 1
                rdata['retDate'] = datetime.datetime.now()
                obj_ = BorrowModel.objects.filter(reader_id=reader_id, book_id=book_id)
                obj_.update(**rdata)
                transaction.savepoint_commit(save_id)
            else:
                raise EOFError("参数不正确")
            result = {"code": 0, "status": "success", "message": "", "data": []}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            result = {"code": -1, "status": "error", "message": str(e), "data": []}
        return Response(result)
