from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import serializers
from accounts.email import EmailService


class EmailSerializer(serializers.Serializer):
    from_address = serializers.EmailField()
    date = serializers.DateTimeField()
    subject = serializers.CharField()
    body = serializers.CharField()


class EmailSentInfoSerializer(serializers.Serializer):
    status = serializers.CharField()


class ReadEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailSerializer

    @extend_schema(
        parameters=[
        OpenApiParameter(
            name='mailbox', 
            type=OpenApiTypes.STR, 
            description='The mailbox type', 
            required=False,
            enum=['inbox', 'archive']  # Enum values
        ),
        OpenApiParameter(
            name='latest_count', 
            type=OpenApiTypes.INT, 
            description='The number of emails to retrieve', 
            required=False
        ),
        OpenApiParameter(
            name='show_unseen', 
            type=OpenApiTypes.BOOL, 
            description='Flag to only show unseen emails', 
            required=False
        )],
    )
    def get(self, request):
        latest_count = int(request.GET.get("latest_count", 5))
        show_unseen = request.GET.get("show_unseen", True)
        criteria = "UNSEEN" if show_unseen else "ALL"
        mailbox = request.GET.get("mailbox", "inbox")
        m = EmailService()
        emails = m.get_emails(criteria=criteria, latest_count=latest_count, mailbox=mailbox)

        return Response(
            emails,
            status.HTTP_200_OK,
        )


class SendEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailSentInfoSerializer

    @extend_schema(
        request=inline_serializer(
            name="SendEmailSerializer",
            fields={
                "to": serializers.EmailField(),
                "subject": serializers.CharField(),
                "body": serializers.CharField(),
            },
        ),
    )
    def post(self, request, format=None):
        to_address = request.data.get("to", "")
        subject = request.data.get("subject", "")
        body = request.data.get("body", "")

        if "@" not in to_address:
            return Response(
                {"msg": "Error when sending email. Wrong email address"},
                status.HTTP_400_BAD_REQUEST,
            )
        
        m = EmailService()
        m.send(to_address, subject, body)

        return Response(
            {"msg": "Email sent successfully"},
            status.HTTP_200_OK,
        )
