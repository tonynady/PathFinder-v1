import json
from channels.generic.websocket import AsyncWebsocketConsumer #,WebsocketConsumer
from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync, sync_to_async

from .models import Project, Robot
from .serializers import ProjectDataSerializer

class StartProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        us = self.scope["user"]
        print(f"the user is {us is not None}............")
        self.room_group_name = 'new-project'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
   
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        project_id = data_json['project_id']
        robot_ip_address = data_json['robot_ip_address']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'project_details',
                'project_id':project_id,
                'robot_ip_address':robot_ip_address,
            }
        )

    async def project_details(self, event):
        project_id = event['project_id']
        robot_ip_address = event['robot_ip_address']

        await self.send(text_data=json.dumps({
            'type':'project_details',
            'project_id':project_id,
            'robot_ip_address':robot_ip_address,
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



class ProjectDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        us = self.scope["user"]
        print(f"the user is {us is not None}............")
        
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.project = await database_sync_to_async(Project.objects.get)(project_id = self.project_id)
        self.project.is_working = True
        await database_sync_to_async(self.project.save)()
        self.robot = await database_sync_to_async(Robot.objects.get)(project = self.project)
        self.room_group_name = f'project_{self.project_id}_data'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
   
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "map":
            self.project.map = text_data_json["map"]
            self.project.is_done = True
            await database_sync_to_async(self.project.save)()
        elif text_data_json["type"] == "project_data_from_robot":
            project_data = text_data_json['data']
            project_data['project'] = self.project_id

            serializer = ProjectDataSerializer(data=project_data)
            await database_sync_to_async(serializer.is_valid)(raise_exception=True)
            await database_sync_to_async(serializer.save)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'project_data_message',
                    'data':json.dumps(serializer.data),
                }
            )

    async def project_data_message(self, event):
        project_data = event['data']

        await self.send(text_data=json.dumps({
            'type':'project_data',
            'data':project_data,
        }))

    async def disconnect(self, close_code):
        # Leave room group
        self.project.is_working = False
        if self.project.is_done:
            self.robot.is_assigned = False
        self.robot.at_maintainance = True
        await database_sync_to_async(self.project.save)()
        await database_sync_to_async(self.robot.save)()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )








# class StartProjectConsumer(WebsocketConsumer):
#     def connect(self):
#         print("I am connecting to 1......")
#         self.room_group_name = 'new-project'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()
   
#     def receive(self, text_data):
#         data_json = json.loads(text_data)
#         project_id = data_json['project_id']
#         robot_ip_address = data_json['robot_ip_address']

#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type':'project_details',
#                 'project_id':project_id,
#                 'robot_ip_address':robot_ip_address,
#             }
#         )

#     def project_details(self, event):
#         project_id = event['project_id']
#         robot_ip_address = event['robot_ip_address']

#         self.send(text_data=json.dumps({
#             'type':'project_details',
#             'project_id':project_id,
#             'robot_ip_address':robot_ip_address,
#         }))

#     def disconnect(self, close_code):
#         # Leave room group
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )



# class ProjectDataConsumer(WebsocketConsumer):
#     def connect(self):
#         print("I am connecting to 2......")
#         self.project_id = self.scope['url_route']['kwargs']['project_id']
#         self.project = Project.objects.get(project_id = self.project_id)
#         self.project.is_working = True
#         self.project.save()
#         self.robot = Robot.objects.get(robot_id = self.project.robot.robot_id)
#         self.room_group_name = f'project_{self.project_id}_data'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()
   
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(type(text_data_json))
#         print(text_data_json)
#         if text_data_json["type"] == "map":
#             self.project.map = text_data_json["map"]
#             self.project.is_done = True
#             self.project.save()
#         elif text_data_json["type"] == "project_data_from_robot":
#             project_data = text_data_json['data']
#             project_data['project'] = self.project_id

#             serializer = ProjectDataSerializer(data=project_data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     'type':'project_data_message',
#                     'data':json.dumps(serializer.data),
#                 }
#             )

#     def project_data_message(self, event):
#         project_data = event['data']

#         self.send(text_data=json.dumps({
#             'type':'project_data',
#             'data':project_data,
#         }))

#     def disconnect(self, close_code):
#         # Leave room group
#         self.project.is_working = False
#         self.robot.is_assigned = False
#         self.robot.at_maintainance = True
#         self.project.save()
#         self.robot.save()

#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
