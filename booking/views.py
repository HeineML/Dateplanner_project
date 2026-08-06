from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Unavailability, DateRequest


def is_heine(user):
    return user.username == 'heine'


@login_required
def dashboard(request):
    """Ruter til riktig dashbord ut fra hvem som er logget inn."""
    if is_heine(request.user):
        return heine_dashboard(request)
    return linnea_dashboard(request)


@login_required
def heine_dashboard(request):
    if request.method == 'POST':
        if 'add_unavailable' in request.POST:
            new_date = request.POST.get('date')
            note = request.POST.get('note', '')
            if new_date:
                Unavailability.objects.get_or_create(date=new_date, defaults={'note': note})
                messages.success(request, 'La til dato som utilgjengelig.')
        elif 'respond' in request.POST:
            req_id = request.POST.get('request_id')
            action = request.POST.get('action')
            date_request = get_object_or_404(DateRequest, id=req_id)
            if action == 'confirm':
                date_request.status = DateRequest.Status.CONFIRMED
            elif action == 'decline':
                date_request.status = DateRequest.Status.DECLINED
            date_request.responded_at = timezone.now()
            date_request.save()
            messages.success(request, 'Svar registrert.')
        return redirect('dashboard')

    pending = DateRequest.objects.filter(status=DateRequest.Status.PENDING)
    confirmed = DateRequest.objects.filter(status=DateRequest.Status.CONFIRMED)
    unavailable_dates = Unavailability.objects.filter(date__gte=date.today())

    return render(request, 'booking/heine_dashboard.html', {
        'pending': pending,
        'confirmed': confirmed,
        'unavailable_dates': unavailable_dates,
        'today': date.today().isoformat(),
    })


@login_required
def linnea_dashboard(request):
    if request.method == 'POST':
        chosen_date = request.POST.get('date')
        activity = request.POST.get('activity', '')
        msg = request.POST.get('message', '')

        if not chosen_date:
            messages.error(request, 'Du må velge en dato.')
        elif Unavailability.objects.filter(date=chosen_date).exists():
            messages.error(request, 'Heine er ikke tilgjengelig denne datoen. Velg en annen 💔')
        else:
            DateRequest.objects.create(
                date=chosen_date,
                activity=activity,
                message=msg,
                requested_by=request.user,
            )
            messages.success(request, 'Forespørselen er sendt! 💌')
        return redirect('dashboard')

    my_requests = DateRequest.objects.filter(requested_by=request.user)
    unavailable_dates = list(
        Unavailability.objects.filter(date__gte=date.today()).values_list('date', flat=True)
    )

    return render(request, 'booking/linnea_dashboard.html', {
        'my_requests': my_requests,
        'unavailable_dates': [d.isoformat() for d in unavailable_dates],
        'today': date.today().isoformat(),
    })
