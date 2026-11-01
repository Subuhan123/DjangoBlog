from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Club, Activity, Signup


def club_list(request):
    """社团列表"""
    clubs = Club.objects.all()
    return render(request, 'campus/club_list.html', {'clubs': clubs})


def activity_list(request):
    """活动列表"""
    activities = Activity.objects.select_related('club').all()
    return render(request, 'campus/activity_list.html', {'activities': activities})


def activity_detail(request, pk):
    """活动详情"""
    activity = get_object_or_404(
        Activity.objects.select_related('club'), pk=pk
    )
    signups = activity.signups.select_related('user').all()
    return render(request, 'campus/activity_detail.html', {
        'activity': activity,
        'signups': signups,
    })


@login_required
def activity_signup(request, pk):
    """报名活动"""
    activity = get_object_or_404(Activity, pk=pk)

    if request.method != 'POST':
        return redirect('campus:activity_detail', pk=pk)

    if timezone.now() > activity.signup_deadline:
        messages.error(request, '报名已截止')
        return redirect('campus:activity_detail', pk=pk)

    if activity.status != 'open':
        messages.error(request, '该活动当前不接受报名')
        return redirect('campus:activity_detail', pk=pk)

    if activity.approved_count >= activity.capacity:
        messages.error(request, '名额已满')
        return redirect('campus:activity_detail', pk=pk)

    if activity.signups.filter(user=request.user).exists():
        messages.warning(request, '你已经报过名了')
        return redirect('campus:activity_detail', pk=pk)

    Signup.objects.create(
        activity=activity,
        user=request.user,
        status='approved',
        remark=''
    )
    messages.success(request, '报名成功')
    return redirect('campus:activity_detail', pk=pk)


@login_required
def my_signups(request):
    """我的报名列表"""
    signups = (
        Signup.objects
        .filter(user=request.user)
        .select_related('activity', 'activity__club')
        .order_by('-created_at')
    )
    return render(request, 'campus/my_signups.html', {'signups': signups})


@login_required
def signup_cancel(request, pk):
    """取消报名"""
    signup = get_object_or_404(Signup, pk=pk, user=request.user)

    if request.method != 'POST':
        return redirect('campus:my_signups')

    activity_title = signup.activity.title
    signup.delete()
    messages.success(request, f'已取消报名：{activity_title}')
    return redirect('campus:my_signups')

