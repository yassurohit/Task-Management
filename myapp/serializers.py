from rest_framework.exceptions import ValidationError
from myapp.models import Comment, Task, Team
from rest_framework import serializers
from user.models import CustomUser


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)
    created_by = serializers.ReadOnlyField(source = 'created_by.username')
    class Meta:
       model = Team
       fields = ['id','name','members','created_at','created_by']
       read_only_fields = ['created_by','created_at']
      
class AddMembersSerializer(serializers.Serializer):
   team_id = serializers.IntegerField()
   user_id = serializers.IntegerField()
   def validate(self,data):
      try:
         team = Team.objects.get(id = data['team_id'])
      except Team.DoesNotExist:
         raise serializers.ValidationError("Team does not exist.")
      try:
         user = CustomUser.objects.get(id = data['user_id'])
      except CustomUser.DoesNotExist:
         raise serializers.ValidationError("user does not exist")
      if team.members.filter(id = user.id):
         raise serializers.ValidationError("User already member of the team.")
      data['team'] = team
      data['user'] = user
      return data
   
class TeamListForUserSerializer(serializers.ModelSerializer):
   class Meta:
      model = Team
      fields = ['id','name','created_at']

class CreateTaskSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = ['id','title','description','due_date','status','assigned_to','created_by','team']
      read_only_fields = ['created_at','updated_at']

class TaskListForUserSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = ['id','title','description','status']

class TaskDetailsSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = '__all__'
class AddMembersSerializer(serializers.Serializer):
   team_id = serializers.IntegerField()
   user_id = serializers.IntegerField()
   def validate(self,data):
      try:
         team = Team.objects.get(id = data['team_id'])
      except Team.DoesNotExist:
         raise serializers.ValidationError("Team does not exist.")
      try:
         user = CustomUser.objects.get(id = data['user_id'])
      except CustomUser.DoesNotExist:
         raise serializers.ValidationError("user does not exist")
      if team.members.filter(id = user.id):
         raise serializers.ValidationError("User already member of the team.")
      data['team'] = team
      data['user'] = user
      return data
   
class TeamListForUserSerializer(serializers.ModelSerializer):
   class Meta:
      model = Team
      fields = ['id','name','created_at']

class CreateTaskSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = ['id','title','description','due_date','status','assigned_to','team','created_by']
      read_only_fields = ['created_at','updated_at','created_by']

class TaskListForUserSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = ['id','title','description','status']

class TaskDetailsSerializer(serializers.ModelSerializer):
   created_by = serializers.ReadOnlyField(source = 'created_by.username')
   assigned_to = serializers.ReadOnlyField(source = 'assigned_to.username')
   class Meta:
      model = Task
      fields = ['id','title','description','due_date','status','assigned_to','team','created_by']
      read_only_fields = ['created_at','updated_at','created_by','assigned_to']

class UpdateTaskSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = ['status','title','description','team','due_date']

   def update(self, instance, validated_data):
        user = self.context.get('request').user
        if 'due_date' in validated_data:
           if(instance.created_by != user):
              raise ValidationError({"message":"You are not authorized to chanage due_date"})
        return super().update(instance, validated_data)
   
class UpdateTaskAssignedSerializer(serializers.Serializer):
   user_id =serializers.IntegerField()
   def validate(self, data):
      task = self.context.get('task')
      user_id = data.get('user_id')
      try:
         new_user=CustomUser.objects.get(id = user_id)
      except CustomUser.DoesNotExist:
         raise ValidationError({"message":"User does not exist"})
      if not task.team.members.filter(id = user_id).exists():
         raise ValidationError({"message":"User is not part of the team"})
      if new_user != task.created_by:
         raise ValidationError({"message":"User dont have access to assign the task"})
      data['new_user'] = new_user
      return data

class GetTaskForTeamSerializer(serializers.ModelSerializer):
   class Meta:
      model = Task
      fields = '__all__'

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
       model = Comment
       fields = ['task','written_by','content','created_at']
       read_only_fields = ['written_by','created_at']

    def validate(self,data):
        user = self.context.get('request').user
        task = data.get('task')
        if  not  task.team.members.filter(id = user.id).exists():
            return ValidationError({"message":"User is not part of the team"})
        return data
class GetCommentsForTaskSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = '__all__'