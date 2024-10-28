from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BillingRecord
from .forms import BillingRecordForm

@login_required
def create_billing(request):
    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form = BillingRecordForm()
    return render(request, 'billing/billing_form.html', {'form': form})

@login_required
def billing_list(request):
    bills = BillingRecord.objects.all()
    return render(request, 'billing/billing_list.html', {'bills': bills})

@login_required
def update_billing(request, billing_id):
    billing = get_object_or_404(BillingRecord, id=billing_id)
    if request.method == 'POST':
        form = BillingRecordForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form = BillingRecordForm(instance=billing)
    return render(request, 'billing/billing_form.html', {'form': form})

@login_required
def delete_billing(request, billing_id):
    billing = get_object_or_404(BillingRecord, id=billing_id)
    if request.method == 'POST':
        billing.delete()
        return redirect('billing_list')
    return render(request, 'billing/confirm_delete.html', {'billing': billing})