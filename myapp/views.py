from django.utils import timezone
from django.shortcuts import render
from myapp.models import Comment, Task, Team
from myapp.serializers import AddMembersSerializer, CreateCommentSerializer, CreateTaskSerializer, GetTaskForTeamSerializer, TaskDetailsSerializer, TaskListForUserSerializer, TeamListForUserSerializer, TeamSerializer, UpdateTaskAssignedSerializer, UpdateTaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators  import api_view,permission_classes
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
@swagger_auto_schema(method='post', request_body=TeamSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team_view(request):
    if request.user.role != "admin":
        return Response({"message":"user is not admin"})
    serializer = TeamSerializer(data = request.data)
    if serializer.is_valid():
        team = serializer.save(created_by = request.user)
        team.members.add(request.user)
        return Response(TeamSerializer(team).data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=AddMembersSerializer)    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_members_view(request):
    serilizer = AddMembersSerializer(data = request.data)
    if serilizer.is_valid():
        team  = serilizer.validated_data['team']
        user = serilizer.validated_data['user']
        if team.created_by != request.user:
            return Response({"message":"Only admin can add members."},status.HTTP_403_FORBIDDEN)
        team.members.add(user)
        return Response({"message":"User added successfully"},status.HTTP_200_OK)
    return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: TeamListForUserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_teams_view(request):
    user = request.user
    teams = user.teams.all()
    serializer = TeamListForUserSerializer(teams,many = True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a team",
    manual_parameters=[
        openapi.Parameter('team_id', openapi.IN_PATH, description="ID of the team to delete", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response(description="Successfully deleted the team", examples={"application/json": {"message": "Successfully deleted the team"}}),
        403: openapi.Response(description="Only the creator of the team can delete the team", examples={"application/json": {"message": "Only the creator of the team can delete the team"}}),
        404: openapi.Response(description="Team does not exist", examples={"application/json": {"message": "Team does not exist"}}),
    },
    operation_summary="Delete a team by its ID",
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team_view(request,team_id):
        try:
            team = Team.objects.get(id = team_id)
        except Team.DoesNotExist:
            return Response({"message":"Team doesnot exists"},status=status.HTTP_403_FORBIDDEN)
        if team.created_by != request.user:
            return Response({"message":"only creator of team can delete team"},status.HTTP_403_FORBIDDEN)
        team.delete()
        return Response({"message":"Successfully deleted the team"},status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=CreateTaskSerializer)    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task_view(request):
    serializer = CreateTaskSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(created_by = request.user)
        return Response(serializer.data,status.HTTP_200_OK)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: TaskListForUserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_for_users(request):
    user  = request.user
    tasks = user.assigned_tasks.all()
    serializer = TaskListForUserSerializer(tasks, many = True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_details(request,task_id):
    try:
        task = Task.objects.get(id = task_id)
        serializer = TaskDetailsSerializer(task)
        return Response(serializer.data,status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"message":"Task doesnot exist"},status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a task",
    manual_parameters=[
        openapi.Parameter('task_id', openapi.IN_PATH, description="ID of the task to delete", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response(description="Successfully deleted the task", examples={"application/json": {"message": "Successfully deleted the task"}}),
        403: openapi.Response(description="Only the creator of the task can delete the task", examples={"application/json": {"message": "Only the creator of the task can delete the task"}}),
        404: openapi.Response(description="Task does not exist", examples={"application/json": {"message": "Task does not exist"}}),
    },
    operation_summary="Delete a task by its ID",
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task_view(request,task_id):
    try:
        task = Task.objects.get(id = task_id)
        if task.created_by != request.user:
            return Response({"message":"only creator can delete task"},status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response({"message":"Successfully deleted task"},status.HTTP_200_OK) 
    except Task.DoesNotExist:
        return Response({"message":"Task doesnot exists"},status.HTTP_404_NOT_FOUND)
    


@swagger_auto_schema(method='put', request_body=UpdateTaskSerializer)  
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_task_view(request,task_id):
    try:
        task = Task.objects.get(id = task_id)
        user = request.user
        if(task.created_by!=user and task.assigned_to != user):
            return Response({"message":"User doesnot have access to change the state of task"},status.HTTP_403_FORBIDDEN)
        serializer = UpdateTaskSerializer(task,data = request.data,partial = True,context = {'request':request})
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message":"successfully updated the task"},status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({"message":"Task doesnot exist"},status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='put', request_body=UpdateTaskAssignedSerializer)  
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_assigned(request,task_id):
    try:
        task = Task.objects.get(id  = task_id)
        serializer = UpdateTaskAssignedSerializer(data = request.data,context = {'task':task})
        if serializer.is_valid():
            new_user = serializer.validated_data['new_user']
            task.assigned_to = new_user
            task.save()
            return Response({"message":"Task assgined successfully"},status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({"message":"Task doesnot exist"},status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_for_team_view(request,team_id):
    try:
        team = Team.objects.get(id = team_id)
        all_tasks = team.tasks.all()
        serializer = GetTaskForTeamSerializer(all_tasks,many = True)
        return Response(serializer.data,status.HTTP_200_OK)
    except Team.DoesNotExist:
        return Response({"message":"Team does not exist"},status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_due_past_taks(request):
    now = timezone.now()
    all_tasks = Task.objects.filter(due_date__gt=now,status__lt=['pending','in_progress'])
    serializer = GetTaskForTeamSerializer(all_tasks,many = True)
    return Response(serializer.data,status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment_view(request):
    serializer = CreateCommentSerializer(data = request.data,context = {'request':request})
    if serializer.is_valid():
        serializer.save(writen_by = request.user)
        return Response({"message":"Comment added successfully"},status.HTTP_200_OK)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_for_task(request,task_id):
    try:
        task = Task.objects.get(id = task_id)
        comments = Comment.objects.filter(task  = task)
        serializer = GetTaskForTeamSerializer(comments,many = True)
        return Response(serializer.data,status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"message":"Task doesnot exist"},status.HTTP_403_FORBIDDEN)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request,comment_id):
    try:
        comment  = Comment.objects.get(id = comment_id)
        if comment.written_by != request.user:
            return Response({"message":"This comment is not written by this user"})
        comment.delete()
        return Response({"comment successfully deleted"},status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"message":"comment doesnot exist"},status.HTTP_403_FORBIDDEN)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_comment_view(request,comment_id):
    try:
        comment = Comment.objects.get(id = comment_id)
        if comment.written_by != request.user:
            return Response({"message":"This comment is not written by this user"},status.HTTP_400_BAD_REQUEST)
        comment.save(content = request.data["content"])
        return Response({"message":"Comment editted successfully"},status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"message":"Comment doesnot exist"},status.HTTP_403_FORBIDDEN)