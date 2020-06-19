from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from safe_internet_app.models import Inquiry
from safe_internet_app.serializers import InquirySerializer


class InquiryView(APIView):

    def post(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        post = request.data
        serializer = InquirySerializer(data=post,
                                       context={'request': request,
                                                'ip': ip})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "Inquiry accepted"})

    def get(self, request):
        inquiries = Inquiry.objects.filter(open_for_review=True)
        serializer = InquirySerializer(inquiries, many=True)

        return Response({"likes": serializer.data})


class InquiryAdminView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        saved_inquiry = get_object_or_404(Inquiry.objects.all(), pk=pk)
        data = request.data
        serializer = InquirySerializer(instance=saved_inquiry,
                                       context={'request': request},
                                       data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "success": "Inquiry reviewed"
        })
