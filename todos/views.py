from django.shortcuts import render, redirect, get_object_or_404
from todos.models import Todo
from todos.forms import TodoForm

def index(request):
    todos = Todo.objects.all()
    return render(request, 'todos/index.html', {'todos': todos})

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})

def update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
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
