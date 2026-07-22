from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task


def index(request):
    if request.method == 'POST':
        task = Task(
            title=request.POST['title'],
            due_at=make_aware(parse_datetime(request.POST['due_at']))
        )
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.filter(deleted=False).order_by('due_at')
    else:
        tasks = Task.objects.filter(deleted=False).order_by('-posted_at')

    context = {
        'tasks': tasks,
        'incomplete_count': tasks.filter(completed=False).count()#未完了数をカウント
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    
    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.completed = True
    task.save()
    return redirect(index)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.deleted = True
    task.deleted_at = timezone.now()
    task.save()
    return redirect(index)


def trash(request):
    tasks = Task.objects.filter(deleted=True).order_by('-deleted_at', '-posted_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'todo/trash.html', context)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

