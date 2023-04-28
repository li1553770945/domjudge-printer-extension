import datetime
import http

from rest_framework.views import APIView, Response
from print.models import PrintModel
from print.serializer import PrintSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, HttpResponse
import os


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class PrintView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        context = dict()
        context['code'] = 0
        print_obj = PrintSerializer(data=request.data)
        if print_obj.is_valid():
            print_obj.save()
            context['id'] = print_obj.data['id']
            context['msg'] = "您的打印已发送至打印队列"
        else:
            context['code'] = 400
            context['msg'] = "添加到打印队列失败，原因：" + str(print_obj.errors)
            print(context['msg'])
            return Response(context, status=http.HTTPStatus.BAD_REQUEST)
        return Response(context)

    def put(self, request):
        context = dict()
        context['code'] = 0
        print_id = request.data.get('id')
        status = request.data.get('status')

        if print_id is None or status is None or status not in ("processing","done"):
            return HttpResponse(status=http.HTTPStatus.BAD_REQUEST)

        print_obj = PrintModel.objects.filter(id=print_id)
        if not print_obj.exists():
            return HttpResponse(status=http.HTTPStatus.NOT_FOUND)
        print_obj = print_obj.first()

        print_obj.status = status
        if status == "processing":
            print_obj.process_start_time = datetime.datetime.now()
        elif status == "done":
            print_obj.done_time = datetime.datetime.now()
        print_obj.save()

        return Response(context)

    def get(self,request):
        context = dict()
        context['code'] = 0
        return Response(context)


class PrintListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        context = dict()
        context['code'] = 0
        status = request.GET.get('status')
        if status is None:
            print_list = PrintModel.objects.filter()
        else:
            print_list = PrintModel.objects.filter(status=status)
        context['data'] = PrintSerializer(print_list, many=True).data
        return Response(context)


def file_download(request, filename):
    file_path = os.path.join('files', filename)
    if os.path.exists(file_path):
        # 使用FileResponse来提供文件下载
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
    else:
        # 如果文件不存在，返回404
        return HttpResponse(status=404)
