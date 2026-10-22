from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()

    # Поиск по названию
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(title__icontains=search)

    # Фильтр по статусу
    status = request.GET.get('status', '')
    if status:
        tasks = tasks.filter(status=status)

    # Сортировка по сроку
    sort = request.GET.get('sort', '')
    if sort == 'deadline_asc':
        tasks = tasks.order_by('deadline')
    elif sort == 'deadline_desc':
        tasks = tasks.order_by('-deadline')
    else:
        tasks = tasks.order_by('-created_at')

    context = {
        'tasks': tasks,
        'search': search,
        'status_filter': status,
        'sort': sort,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'tasks/index.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Создание'})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Редактирование'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})


def task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect('task_list')