from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
import json
from rest_framework.parsers import JSONParser
from task.models import Task

from task.api.serializers import TaskSerializer




class TaskListView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = TaskSerializer
    
    queryset = Task.objects.all()

    # def get_queryset(self):
    #     #time.sleep(1)
    #     return(MonitoringType.objects.all())




class TaskUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskCreate(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        counter = 0;
        for i in range(10000):
            for k in range(1000):
                counter = counter + 500;

        return Response({"counter_value": counter})

    