from rest_framework import serializers
from .models import Notice, NoticeFile


class NoticeFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeFile
        fields = ["id", "file", "uploaded_at"]


class NoticeSerializer(serializers.ModelSerializer):
    files = NoticeFileSerializer(many=True, read_only=True)

    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "description",
            "notice_type",
            "created_at",
            "files",
        ]
