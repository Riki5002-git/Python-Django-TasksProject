from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from DjangoApp.forms import UserForm, TaskForm, LoginForm, PersonalAreaForm
from DjangoApp.models import Task, User, Team
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('personalArea')
    else:
        form = UserForm()
    return render(request, "register.html", {"form": form})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            user = User.objects.filter(
                username=username,
                first_name=first_name,
                last_name=last_name
            ).first()
            if user:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if not user.role or not user.team:
                    return redirect('personalArea')
                return redirect('home')
            else:
                form.add_error(None, "לא נמצא משתמש עם פרטים אלו במערכת")
    return render(request, "login.html", {"form": form})

def logout(request):
    auth_logout(request)
    return redirect('home')


def personalArea(request):
    user = request.user
    if request.method == 'POST':
        form = PersonalAreaForm(request.POST)
        if form.is_valid():
            user.role = form.cleaned_data['role']
            user.team = form.cleaned_data['team']
            user.save()
            return redirect('home')
    else:
        initial_data = {
            'role': user.role,
            'team': user.team
        }
        form = PersonalAreaForm(initial=initial_data)

        return render(request, 'personalArea.html', {'form': form})

def getAllTasks(request):
    if request.user.role != "מנהל":
        return HttpResponseForbidden("אין לך הרשאה")
    tasks = Task.objects.all()
    return render(request, "getAllTasks.html", {"tasks": tasks})


def addTask(request):
    if request.user.role != "מנהל":
        return HttpResponseForbidden("רק מנהל יכול להוסיף משימות")
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.team_name = request.user.team
            task.status = 'חדש'
            task.save()
            return redirect('getAllTasks')
    else:
        form = TaskForm()
    return render(request, "addTask.html", {"form": form})

def deleteTask(request, id):
    if request.user.role != "מנהל":
        return HttpResponseForbidden("אין לך הרשאה")
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('getAllTasks')

def editTask(request, id):
    if request.user.role != "מנהל":
        return HttpResponseForbidden("אין לך הרשאה")
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('getAllTasks')
    else:
        form = TaskForm(instance=task)
    return render(request, "editTask.html", {"form": form, "task": task})


def getTeamsTasks(request, team):
    team_obj = get_object_or_404(Team, team_name=team)
    tasks = Task.objects.filter(team_name=team_obj)
    return render(request, "getAllTasks.html", {"tasks": tasks, "team": team_obj})


def taskAssignment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    Task.objects.filter(id=task_id).update(user=request.user)
    Task.objects.filter(id=task_id).update(status="בתהליך")
    task.refresh_from_db()
    return redirect('getTeamsTasks', team=str(task.team_name))

def changeStatus(request, task_id, status):
    task = get_object_or_404(Task, id=task_id)
    task.status = status
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def filterByStatus(request, status):
    if request.user.role == "מנהל":
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.filter(status=status, team_name=request.user.team)
    return render(request, "getAllTasks.html", {"tasks": tasks, "current_filter": status})


def filterByWorker(request, username):
    if request.user.role == "מנהל":
        tasks = Task.objects.filter(user__first_name__icontains=username)
    else:
        tasks = Task.objects.filter(
            user__first_name__icontains=username,
            team_name=request.user.team
        )
    return render(request, "getAllTasks.html", {"tasks": tasks, "current_filter": username})