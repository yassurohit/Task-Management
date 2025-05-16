from django.urls import path
from myapp.views import add_members_view, create_task_view, create_team_view, delete_task_view, delete_team_view, get_due_past_taks, get_task_details, get_tasks_for_team_view, get_tasks_for_users, get_user_teams_view, update_task_assigned, update_task_view


urlpatterns = [
    path('create_team_view/',create_team_view,name='create_team'),
    path('add_members/',add_members_view,name = 'add_members'),
    path('teams/',get_user_teams_view,name = 'get-user-teams'),
    path('delete-team/<int:team_id>/',delete_team_view,name = 'delete-team'),
    path('create-task/',create_task_view,name = 'create-task'),
    path('get-tasks/',get_tasks_for_users,name='get-tasks'),
    path('task-details/<int:task_id>/',get_task_details,name = 'task-details'),
    path('delete-task/<int:task_id>',delete_task_view,name='delete-task'),
    path('update-task/<int:task_id>/',update_task_view,name='task-view'),
    path('update-task-assigned/<int:task_id>',update_task_assigned,name='task-assigned'),
    path('get-tasks-for-team/<int:team_id>',get_tasks_for_team_view,name = 'get-tasks-for-team'),
    path('overdue-tasks/',get_due_past_taks,name='over-due-tasks'),
] 