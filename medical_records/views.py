from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm
from django.core.paginator import Paginator

@login_required
def create_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('records_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_records/record_form.html', {'form': form})

@login_required
def records_list(request):
    records_list = MedicalRecord.objects.all()
    paginator = Paginator(records_list, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'medical_records/records_list.html', {'page_obj': page_obj})


@login_required
def update_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect(reverse('records_list'))
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'medical_records/record_form.html', {'form': form})

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect(reverse('records_list'))
    return render(request, 'medical_records/confirm_delete.html', {'record': record})
