from datetime import datetime, time
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from todos.models import Todo
from todos.forms import TodoForm, TodoSearchForm
from utils.message_helper import add_message, ICON_MAP
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# 各種日付の範囲検索
def get_search_date(queryset,field,date_start,date_end):
    # 開始日が入力されている場合、開始日は入力した日の00:00:00を設定
    if date_start:
        date_start = datetime.combine(date_start,time.min)
    # 終了日が入力されている場合、終了日は入力した日の23:59:59を設定
    if date_end:
        date_end = datetime.combine(date_end,time.max)

    # 開始日及び終了日をもとに範囲検索を行う
    if date_start and date_end and (date_start <= date_end):
        return queryset.filter(**{f"{field}__range":(date_start, date_end)})
    elif date_start:
        return queryset.filter(**{f"{field}__gte":(date_start)})
    elif date_end:
        return queryset.filter(**{f"{field}__lte":(date_end)})
    return queryset

@login_required
def index(request):
    action = request.GET.get('action')
    form = TodoSearchForm(request.GET if action == 'search' else None)
    todos = Todo.objects.filter(user=request.user)

    # 検索ボタン押下時、検索を行う
    if action == 'search':
        if form.is_valid():
            cd = form.cleaned_data
            # タスク名を入れている場合、部分検索を行う
            if cd['title']:
                todos = todos.filter(title__icontains=cd['title'])
            # 緊急度を入力している場合、条件検索を行う
            if cd['urgency']:
                todos = todos.filter(urgency=cd['urgency'])
            # 重要度を入力している場合、条件検索を行う
            if cd['importance']:
                todos = todos.filter(importance=cd['importance'])
            # ステータスを入力している場合、条件検索を行う
            if cd['status']:
                todos = todos.filter(status=cd['status'])
            # 更新日時を入力している場合、範囲検索を行う
            todos = get_search_date(todos,'updated_at',cd['updated_from'],cd['updated_to'])
            # 作成日時を入力している場合、範囲検索を行う
            todos = get_search_date(todos,'created_at',cd['created_from'],cd['created_to'])
            # 締切日時を入力している場合、範囲検索を行う
            todos = get_search_date(todos,'due_date',cd['due_date_from'],cd['due_date_to'])
            # 完了日時を入力している場合、範囲検索を行う
            todos = get_search_date(todos,'completed_at',cd['completed_from'],cd['completed_to'])

    # 作成日時の降順に並び替え
    todos = todos.order_by('-created_at')
    # 検索結果の件数を取得
    count = todos.count()
    if action == 'search' and count == 0:
        add_message(request, 'MSG_3101')

    return render(request, 'todos/index.html', {
        'todos': todos,
        'count': count,
        'form': form,
        'icon_map': ICON_MAP
    })

def get_progress(request, actual_value, target_value):
    # 実績値がNoneの場合true
    is_actual_invalid = actual_value is None
    # 目標値がNoneまたは0の場合true
    is_target_invalid = target_value is None or target_value == 0

    if is_actual_invalid and is_target_invalid:
        field = '目標値および実績値'
    elif is_actual_invalid:
        field = '実績値'
    elif is_target_invalid:
        field = '目標値'
    else:
        return None
    add_message(request, 'MSG_4101', field=field)

@login_required
def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.completed_at = timezone.now() if todo.status == 1 else None
            todo.save()
            get_progress(request, todo.actual_value, todo.target_value)
            add_message(request, 'MSG_1101', action='追加')
            return redirect('todos:index')
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})

@login_required
def update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 本人以外の場合アクセスできないようにする
    if todo.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.completed_at = timezone.now() if todo.status == 1 else None
            todo.save()
            get_progress(request, todo.actual_value, todo.target_value)
            add_message(request, 'MSG_1101', action='更新')
            return redirect('todos:index')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/update.html', {'form': form})

@login_required
def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 本人以外の場合アクセスできないようにする
    if todo.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        todo.delete()
        add_message(request, 'MSG_1101', action='削除')
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
    return redirect('todos:index')

# タスク完了のチェックをオンにした場合
@login_required
def change_complete_true(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 本人以外の場合アクセスできないようにする
    if todo.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        # 目標値がNoneまたは0の場合実績値の補正を行わない
        if todo.target_value is not None and todo.target_value != 0:
            # 実績値がNoneまたは実績値＜目標値の場合、実績値＝目標値（進捗率100%）となるように実績値の補正を行う
            if todo.actual_value is None or todo.actual_value < todo.target_value:
                todo.actual_value = todo.target_value
        todo.save()
        add_message(request, 'MSG_1101', action='完了')
    return change_complete(request, pk, 1)

# タスク完了のチェックをオフにした場合
@login_required
def change_complete_false(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 本人以外の場合アクセスできないようにする
    if todo.user != request.user:
        raise PermissionDenied
    add_message(request, 'MSG_1102')
    return change_complete(request, pk, 0)