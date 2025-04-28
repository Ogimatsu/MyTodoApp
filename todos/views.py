from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from todos.models import Todo
from todos.forms import TodoForm

def index(request):
    todos = Todo.objects.all()
    return render(request, 'todos/index.html', {'todos': todos})

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            if todo.status == 1:
                todo.completed_at = timezone.now()
            else:
                todo.completed_at = None
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})

def update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            if todo.status == 1:
                todo.completed_at = timezone.now()
            else:
                todo.completed_at = None
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/update.html', {'form': form})

def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:index')

# タスク完了かどうかが変更になった場合に行う処理
def change_complete(request,pk,status):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.status = status
        todo.updated_at = timezone.now()
        # タスク完了の場合、完了日時を設定
        todo.completed_at = timezone.now() if status == 1 else None
        todo.save()
    base_url = reverse('todos:index')
    return redirect(f'{base_url}#todo-{pk}')

# タスク完了のチェックをオンにした場合
def change_complete_true(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        # 目標値がNoneまたは0の場合実績値の補正を行わない
        if todo.target_value is not None and todo.target_value != 0:
            # 実績値がNoneまたは実績値＜目標値の場合、実績値＝目標値（進捗率100%）となるように実績値の補正を行う
            if todo.actual_value is None or todo.actual_value < todo.target_value:
                todo.actual_value = todo.target_value
        todo.save()
    return change_complete(request, pk, 1)

# タスク完了のチェックをオフにした場合
def change_complete_false(request, pk):
    return change_complete(request, pk, 0)