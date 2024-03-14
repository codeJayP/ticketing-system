from django.shortcuts import render, get_object_or_404, redirect
from .decorators import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout

@login_required(login_url='login')
@admin_only
def index (request):
    users = User.objects.exclude(groups__name='admin', )
    total_repair_requests = RepairRequest.objects.count()
    ongoing = RepairRequest.objects.filter(status='ongoing').count()
    complete = RepairRequest.objects.filter(status='complete').count()


    context = {
        'users': users,
        'total_repair_requests': total_repair_requests,
        'ongoing': ongoing,
        'complete': complete
    }
    return render(request, 'admin/home.html', context)

@login_required(login_url='login')
@admin_only
def user_staff (request):
    users = User.objects.exclude(Q(groups__name='admin') | Q(groups__name='controller'))

    context = {
        'users': users
    }
    return render(request, 'admin/user_staff.html', context)

@login_required(login_url='login')
@admin_only
def user_controller (request):
    users = User.objects.exclude(Q(groups__name='admin') | Q(groups__name='staff'))

    context = {
        'users': users
    }
    return render(request, 'admin/user_controller.html', context)

@login_required(login_url='login')
@admin_only
def modify_user_role_staff(request, user_id):
    user = User.objects.get(pk=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('new_role')
        group = Group.objects.get(name=new_role)
        user.groups.clear()
        user.groups.add(group)
        return redirect('user_staff')
    
    groups = Group.objects.exclude(name='admin')
    context = {
        'user': user,
        'groups': groups,
    }
    
    return render(request, 'admin/modify_user_role_staff.html', context)

@login_required(login_url='login')
@admin_only
def modify_user_role_controller(request, user_id):
    user = User.objects.get(pk=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('new_role')
        group = Group.objects.get(name=new_role)
        user.groups.clear()
        user.groups.add(group)
        return redirect('user_controller')
    
    groups = Group.objects.exclude(name='admin')
    context = {
        'user': user,
        'groups': groups,
    }
    
    return render(request, 'admin/modify_user_role_controller.html', context)

def ticket_logs(request):
     logs = TicketLogs.objects.all().order_by('-date')

     context = {
         'logs': logs
     }
     return render(request, 'admin/ticket_logs.html', context)


def repair(request):
      return render(request, 'repair.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def controller(request):
    hopps_list = RepairRequest.objects.all()

    if request.method == 'POST':
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            hopps = form.save(commit=False)
            hopps.save()
            return redirect('controller')
    else:
        form = RepairRequestForm()

    context = {
         'hopps_list': hopps_list,
         'form': form
    }
    return render(request, 'controller/controller.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def controller_ticket(request):
    hopps_list = RepairRequest.objects.all().order_by('-date')

    if request.method == 'POST':
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            hopps = form.save(commit=False)
            # Check if staff is assigned and if the user is a controller
            if hopps.staff and request.user.is_controller:
                hopps.status = 'ongoing'  # Set status as ongoing
                hopps.save()
                return redirect('controller')
            else:
                return HttpResponse("Permission Denied")
    else:
        form = RepairRequestForm()

    context = {
        'hopps_list': hopps_list,
        'form': form
    }
    return render(request, 'controller/controller_ticket.html', context)


# Department
def repair_request_again(request):
    hopps_form = RepairRequestForm()

    if request.method == 'POST':
        hopps_form = RepairRequestForm(request.POST)

        if hopps_form.is_valid():
            hopps_form.save()
            messages.success(request, 'Succesfuly submited, just wait for our staff.')
            return redirect('repair_request')

    hopps_list = RepairRequest.objects.all()
    context = {
        'hopps_form': hopps_form,
        'hopps_list': hopps_list,
    }

    return render(request, 'repair_request/repair_request_again.html', context)

def asign(request, pk):
    hopss = RepairRequest.objects.get(id=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=hopss)
        if form.is_valid():
            form.save()
            return redirect('controller_ticket')
    else:
        form = StaffForm(instance=hopss)
    context = { 'form': form}
    return render(request, 'repair_request/repair_request_update.html', context)

@login_required(login_url='login')
def repair_request_details(request, event_id):
    hopps2 = get_object_or_404(RepairRequest, id=event_id)
    hopps3 = get_object_or_404(RepairRequest, id=event_id)
    hopps_list = RepairRequest.objects.all()

    context = {
        'hopps2':hopps2,
        'hopps_list': hopps_list,
        'hopps3': hopps3
    }
    
    return render(request, 'repair_request/repair_request_details.html', context)


# SAMPLE__________________________________________________________________________________

def repair_request(request):
    hopps_form = RepairRequestForm()

    if request.method == 'POST':
        hopps_form = RepairRequestForm(request.POST)

        if hopps_form.is_valid():
            hopps_form.save()
            messages.success(request, 'Successfully submitted, just wait for our staff.')
            return redirect('repair_request_again')

    context = {
        'hopps_form': hopps_form,
    }

    return render(request, 'repair_request/repair_request.html', context)

def get_offices_by_department(request):
    department_id = request.GET.get('department_id')

    if not department_id:
        return JsonResponse({'error': 'department_id is required'}, status=400)

    try:
        department_id = int(department_id)
    except ValueError:
        return JsonResponse({'error': 'department_id must be a number'}, status=400)

    offices = Office.objects.filter(department_id=department_id).values('id', 'name')

    data = {'offices': {office['id']: office['name'] for office in offices}}
    return JsonResponse(data)

# STAFF
@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def staff(request):
    if request.user.groups.filter(name='staff').exists():
        repair_requests = RepairRequest.objects.filter(staff=request.user, complete=False).order_by('-date')
    else:
        repair_requests = RepairRequest.objects.filter(complete=False).order_by('-date')

    context = {
        'repair_requests': repair_requests
    }
    return render(request, 'staff/staff.html', context)

def complete_request(request, request_id):
    repair_request = get_object_or_404(RepairRequest, id=request_id)

    # Perform logic to mark the repair request as complete
    repair_request.complete = True
    repair_request.save()

    return redirect('staff')

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def forasignstaff(request, pk):
    hopss = RepairRequest.objects.get(id=pk)
    if request.method == 'POST':
        form = RepairRequestInfoForm(request.POST, instance=hopss)
        if form.is_valid():
            form.save()
            return redirect('controller_ticket')
    else:
        form = RepairRequestInfoForm(instance=hopss)
    context = { 'form': form}
    return render(request, 'repair_request/repair_request_update_staff.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def repair_request_details_staff(request, event_id):
    hopps2 = get_object_or_404(RepairRequest, id=event_id)
    hopps3 = get_object_or_404(RepairRequest, id=event_id)
    hopps_list = RepairRequest.objects.all()

    context = {
        'hopps2':hopps2,
        'hopps_list': hopps_list,
        'hopps3': hopps3
    }
    
    return render(request, 'staff/repair_request_details_staff.html', context)

# authentication___________________________________________________________________________
@csrf_protect
def user_login(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            # request.session['group'] = user.groups()
            return redirect('index')
        else:
            if user is None:
                messages.error(request, 'Username does not exist.')
            else:
                messages.error(request, 'Incorrect password.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def add_user(request):
    role_filter = request.GET.get('role', None) 
    users = User.objects.exclude(groups__name='admin', )
    
    if role_filter:
        users = users.filter(userprofile__role=role_filter)

    add_user = AddUserForm()

    if request.method == 'POST':
        add_user = AddUserForm(request.POST, request.FILES)
        if add_user.is_valid():
            user = add_user.save()
            username = add_user.cleaned_data.get('username')
            role = add_user.cleaned_data.get('role')
            return redirect('add_user')
        else:
            for error in add_user.errors.values():
                messages.error(request, error)

    context = {
        'add_user': add_user, 
        'selected_role': role_filter,
    }
    return render(request, 'admin/add_user.html', context)