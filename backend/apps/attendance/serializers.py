from rest_framework import serializers
from .models import AttendanceSession, AttendanceRecord


class AttendanceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSession
        fields = ["id", "subject", "is_active", "start_time", "end_time"]

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ["id", "student", "session", "method", "marked_at"]
        read_only_fields = ["student", "marked_at"]