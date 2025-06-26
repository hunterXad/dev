from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import StreamRoom
from django.shortcuts import get_object_or_404
from .models import StreamRoom, PendingJoinRequest
from django.utils.timezone import now
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        
        # تأكد إن الغرفة ما موجودة مسبقًا
        if StreamRoom.objects.filter(name=room_name).exists():
            return render(request, 'stream/create_room.html', {
                'error': "الغرفة موجودة مسبقًا. اختر اسمًا مختلفًا."
            })
        
        # إنشاء الغرفة وربطها بالمستخدم
        room = StreamRoom.objects.create(
            name=room_name,
            owner=request.user
        )
        
        # توجيه المستخدم إلى غرفة البث مباشرة
        return redirect('stream_room', room_name=room.name)
    
    return render(request, 'stream/create_room.html')



def lobby(request, room_name):
    room = get_object_or_404(StreamRoom, name=room_name)

    if request.method == "POST":
        name = request.POST.get("username")

        # إذا كان المستخدم هو الـ owner → يدخل مباشرة
        if request.user.is_authenticated and request.user == room.owner:
            return redirect('stream_room', room_name=room.name)

        # IP Address
        ip = request.META.get('REMOTE_ADDR')

        # إنشاء أو تحديث طلب الدخول
        PendingJoinRequest.objects.update_or_create(
            room=room,
            name=name,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'ip_address': ip,
                'approved': False,
                'rejected': False,
                'created_at': now()
            }
        )

        return redirect('waiting_page', room_name=room.name, user_name=name)

    return render(request, 'stream/lobby.html', {'room_name': room.name})




@login_required
def room(request, room_name):
    room = get_object_or_404(StreamRoom, name=room_name)
    is_owner = room.owner == request.user

    if is_owner:
        pending_requests = room.pending_requests.filter(approved=False, rejected=False)
    else:
        # هل يوجد طلب دخول لهذا المستخدم وتمت الموافقة عليه؟
        join_request = room.pending_requests.filter(
            user=request.user, approved=True, rejected=False
        ).first()

        if not join_request:
            return redirect('waiting_page', room_name=room.name, user_name=request.user.username)

        pending_requests = None  # الزائر ما يشوف الطلبات

    return render(request, 'stream/room.html', {
        'room_name': room.name,
        'is_owner': is_owner,
        'pending_requests': pending_requests,
    })




@require_POST
@login_required
def handle_join_request(request, room_name):
    room = get_object_or_404(StreamRoom, name=room_name)

    # تأكد أن المستخدم هو المالك
    if request.user != room.owner:
        return HttpResponse("غير مسموح", status=403)

    action = request.POST.get("action")
    name = request.POST.get("name")

    try:
        join_request = PendingJoinRequest.objects.get(room=room, name=name)
        if action == "approve":
            join_request.approved = True
            join_request.rejected = False
            messages.success(request, f"تمت الموافقة على {name}")
        elif action == "reject":
            join_request.rejected = True
            join_request.approved = False
            messages.error(request, f"تم رفض {name}")
        join_request.save()
    except PendingJoinRequest.DoesNotExist:
        messages.error(request, "الطلب غير موجود")

    return redirect("stream_room", room_name=room.name)


def check_join_status(request, room_name, user_name):
    room = get_object_or_404(StreamRoom, name=room_name)
    try:
        join_request = PendingJoinRequest.objects.get(room=room, name=user_name)
        if join_request.approved:
            return JsonResponse({'status': 'approved'})
        elif join_request.rejected:
            return JsonResponse({'status': 'rejected'})
        else:
            return JsonResponse({'status': 'waiting'})
    except PendingJoinRequest.DoesNotExist:
        return JsonResponse({'status': 'not_found'})


def waiting_page(request, room_name, user_name):
    return render(request, 'stream/waiting_page.html', {
        'room_name': room_name,
        'user_name': user_name,
    })
    
    
