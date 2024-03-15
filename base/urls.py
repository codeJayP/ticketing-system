from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('user_staff/', user_staff, name='user_staff'),
    path('user_controller/', user_controller, name='user_controller'),
    path('modify_user_role_staff/<int:user_id>/', modify_user_role_staff, name='modify_user_role_staff'),
    path('modify_user_role_controller/<int:user_id>/', modify_user_role_controller, name='modify_user_role_controller'),

    path('controller/', controller, name='controller'),
    path('controller_ticket/', controller_ticket, name='controller_ticket'),

    path('staff/', staff, name='staff'),
    path('repair_request_details_staff/<int:event_id>/', repair_request_details_staff, name='repair_request_details_staff'),
    path('complete_request/<int:request_id>/', complete_request, name='complete_request'),

    path('repair/', repair, name="repair"),
    path('ticket_logs/', ticket_logs, name="ticket_logs"),
    # department
    path('repair-request/', repair_request, name="repair_request"),
    path('repair_request_details/<int:event_id>/', repair_request_details, name='repair_request_details'),
    path('asign/<int:pk>/', asign, name='asign'),
    path('forasignstaff/<int:pk>/', forasignstaff, name='forasignstaff'),
    path('forasignstaffstatus/<int:pk>/', forasignstaffstatus, name='forasignstaffstatus'),
    path('repair_request_again/', repair_request_again, name="repair_request_again"),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name="logout"),

    path('get-offices/', get_offices_by_department, name='get_offices_by_department'),
    path('add_user/', add_user, name='add_user'),

    

]