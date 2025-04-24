from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
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
            if todo.completed:
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
            if todo.completed:
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
    return render(request, 'todos/delete.html', {'todo': todo})

# タスク完了かどうかが変更になった場合に行う処理
def change_complete(request,pk,completed=False):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.completed = completed
        todo.updated_at = timezone.now()
        # タスク完了の場合、完了日時を設定
        todo.completed_at = timezone.now() if completed else None
        todo.save()
    return redirect('todos:index')

# タスク完了のチェックをオンにした場合
def change_complete_true(request, pk):
    return change_complete(request, pk, completed=True)

# タスク完了のチェックをオフにした場合
def change_complete_false(request, pk):
    return change_complete(request, pk, completed=False)