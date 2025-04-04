from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Medicine
from .forms import MedicineForm



@login_required
def create_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'inventory/medicine_form.html', {'form': form})

@login_required
def medicine_list(request):
    medicines_list = Medicine.objects.all()
    paginator = Paginator(medicines_list, 10)  # Show 10 medicines per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/medicine_list.html', {'page_obj': page_obj})


@login_required
def update_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'inventory/medicine_form.html', {'form': form})

@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'inventory/confirm_delete.html', {'medicine': medicine})
