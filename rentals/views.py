from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import House, Rider, Booking, HouseImage, SMSLog
from .forms import CustomUserCreationForm
from rentals.utils.sms import send_sms_alert
from .forms import HouseForm, HouseImageFormSet
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model  # ✅ correct
User = get_user_model()
from django.db.models import Q
from django.core.paginator import Paginator
import csv
import io
from django.http import HttpResponse
from rentals.utils.sms import send_sms_alert
from django.shortcuts import render
from .decorators import role_required


from django.shortcuts import render

def home(request):
    # Always show home.html after login
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user_role': request.user.role})
    else:
        return render(request, 'home.html')

def house_list(request):
    location_query = request.GET.get('location')
    if location_query:
        houses = House.objects.filter(location__icontains=location_query, is_booked=False).prefetch_related('images')
    else:
        houses = House.objects.all().prefetch_related('images')
    return render(request, 'house_list.html', {'houses': houses})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def book_house(request, house_id):
    house = get_object_or_404(House, id=house_id)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        occupation = request.POST.get('occupation')
        national_id = request.POST.get('national_id')
        move_in = request.POST.get('move_in')
        notes = request.POST.get('notes')

        house.is_booked = True
        house.save()

        landlord = house.landlord
        tenant = request.user

        message = (
            f"Hello {landlord.username}, your house '{house.title}' in {house.location} has been requested by "
            f"{tenant.username}.\nNational ID: {national_id}\nPhone: {phone}\nOccupation: {occupation}\n"
            f"Move-in Date: {move_in}\nNotes: {notes}"
        )
        send_sms_alert(landlord.phone, message)
        admin_phone = "0745300566"  # Replace with your actual admin number
        send_sms_alert(admin_phone, message)

        return render(request, 'booking_confirmation.html', {
    'house': house,
    'tenant': tenant,
    'move_in': move_in,
    'national_id': national_id,
    'phone': phone,
    'occupation': occupation,
    'notes': notes
})

    return render(request, 'book_form.html', {
        'house': house,
        'tenant': request.user
    })
@login_required
def rider_workspace(request):
    rider = get_object_or_404(Rider, user=request.user)
    bookings = list(Booking.objects.filter(house__location__icontains=rider.area).values(
    'house__latitude', 'house__longitude', 'tenant__username'
))
    return render(request, 'rider_workspace.html', {
        'rider': rider,
        'bookings': bookings
    })
@login_required
def unbook_house(request, house_id):
    house = get_object_or_404(House, id=house_id)
    house.is_booked = False
    house.save()
    return redirect('house_list')

@login_required
def create_house(request):
    if not request.user.is_superuser and request.user.role != 'landlord':
        return render(request, 'access_denied.html', {
            'message': "Only landlords and admins can create houses."
        })

    if request.method == 'POST':
        house_form = HouseForm(request.POST)
        image_formset = HouseImageFormSet(request.POST, request.FILES, queryset=HouseImage.objects.none())

        if house_form.is_valid() and image_formset.is_valid():
            house = house_form.save(commit=False)
            house.landlord = request.user  # works for both landlord and admin
            house.save()

            for form in image_formset.cleaned_data:
                if form and form.get('image'):
                    HouseImage.objects.create(house=house, **form)

            return redirect('house_list')
    else:
        house_form = HouseForm()
        image_formset = HouseImageFormSet(queryset=HouseImage.objects.none())

    return render(request, 'create_house.html', {
        'house_form': house_form,
        'image_formset': image_formset
    })
@staff_member_required  # Only superusers or staff can access
def manage_users(request):
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)  # Exclude self

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user = get_object_or_404(User, id=user_id)
        user.role = new_role
        user.save()
        return redirect('manage_users')

    return render(request, 'admin/manage_users.html', {'users': users})
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return render(request, 'access_denied.html', {
            'message': "Only admins can access this dashboard."
        })

    # 📊 Metrics
    total_users = User.objects.count()
    total_houses = House.objects.count()
    total_bookings = Booking.objects.count()

    # 📈 Monthly bookings chart data
    monthly_bookings = (
        Booking.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    labels = [b['month'].strftime('%b') for b in monthly_bookings]
    data = [b['count'] for b in monthly_bookings]

    # 👥 Recent user signups
    recent_users = User.objects.order_by('-date_joined')[:10]

    # 📲 SMS alert logs (if model exists)
    sms_logs = SMSLog.objects.order_by('-timestamp')[:10] if 'SMSLog' in globals() else []

    return render(request, 'dashboards/admin_dashboard.html', {
        'total_users': total_users,
        'total_houses': total_houses,
        'total_bookings': total_bookings,
        'labels': labels,
        'data': data,
        'recent_users': recent_users,
        'sms_logs': sms_logs
    })


@login_required
def landlord_dashboard(request):
    if request.user.role != 'landlord' and not request.user.is_superuser:
        return render(request, 'access_denied.html', {
            'message': "Only landlords and admins can access this dashboard."
        })

    total_houses = House.objects.filter(landlord=request.user).count()
    total_bookings = Booking.objects.filter(house__landlord=request.user).count()
    total_tenants = Booking.objects.filter(house__landlord=request.user).values('tenant').distinct().count()

    return render(request, 'dashboards/landlord_dashboard.html', {
        'total_houses': total_houses,
        'total_bookings': total_bookings,
        'total_tenants': total_tenants
    })
User = get_user_model()
@role_required(['Landlord'])
def landlord_dashboard(request):
    houses = request.user.house_set.all()  # assuming House has FK to owner
    return render(request, 'dashboard/landlord_dashboard.html', {'houses': houses})


@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return render(request, 'access_denied.html', {
            'message': "Only admins can manage users."
        })

    role = request.GET.get('role')
    query = request.GET.get('q')
    page_number = request.GET.get('page')

    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')  # ✅ always defined

    if role:
        users = users.filter(role=role)

    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_users.html', {
        'page_obj': page_obj,
        'role': role,
        'query': query
    })


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.save()
        return redirect('manage_users')

    return render(request, 'admin/edit_user.html', {
        'user': user
    })

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
@login_required
def export_users_excel(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)

    users = User.objects.all().values_list('username', 'email', 'role', 'date_joined')

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['username', 'email', 'role', 'date_joined'])
    for username, email, role, date_joined in users:
        date_str = date_joined.isoformat() if hasattr(date_joined, 'isoformat') else str(date_joined)
        writer.writerow([username, email, role, date_str])

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'
    return response
@role_required(['CEO'])
def ceo_dashboard(request):
    houses = House.objects.all()
    users = CustomUser.objects.all()
    bookings = Booking.objects.all()
    sms_logs = SmsLog.objects.all()
    return render(request, 'dashboard/ceo_dashboard.html', {
        'houses': houses,
        'users': users,
        'bookings': bookings,
        'sms_logs': sms_logs,
    })

@role_required(['CEO'])
def assign_role(request, user_id, role):
    user = CustomUser.objects.get(id=user_id)
    if role in dict(CustomUser.ROLE_CHOICES).keys():
        user.role = role
        user.save()
    return redirect('ceo_dashboard')

@role_required(['Manager'])
def manager_dashboard(request):
    users = CustomUser.objects.filter(role='Tenant')
    return render(request, 'dashboard/manager_dashboard.html', {'users': users})

@role_required(['Manager'])
def assign_landlord(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.role = 'Landlord'
    user.save()
    return redirect('manager_dashboard')


    return response

