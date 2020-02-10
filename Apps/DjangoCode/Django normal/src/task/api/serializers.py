from rest_framework import serializers
from task.models import Task
import json

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


