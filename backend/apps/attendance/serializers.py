from rest_framework import serializers
from .models import AttendanceSession, AttendanceRecord
from django.utils import timezone


class AttendanceSessionSerializer(serializers.ModelSerializer):
    remaining_seconds = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = [
            "id",
            "subject",
            "is_active",
            "start_time",
            "end_time",
            "duration_minutes",
            "remaining_seconds"
        ]

    def get_remaining_seconds(self, obj):
        remaining = (obj.end_time - timezone.now()).total_seconds()
        return max(0, int(remaining))


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ["id", "student", "session", "method", "marked_at"]
        read_only_fields = ["student", "marked_at"]
