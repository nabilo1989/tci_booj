from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from .decorators import verified_user_required


def contact_list(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.all().order_by('last_name', 'first_name')

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(phone__icontains=query) |
            Q(workplace__icontains=query) |
            Q(position__icontains=query)
        )

    return render(request, 'phonebook/contact_list.html', {'contacts': contacts})


@verified_user_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.created_by = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'phonebook/contact_form.html', {'form': form})


@verified_user_required
@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'phonebook/contact_form.html', {'form': form})

@verified_user_required
@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'phonebook/contact_confirm_delete.html', {'contact': contact})


from django.shortcuts import render
from .models import Contact
from django.db.models import Q


def search_contacts(request):
    query = request.GET.get('q', '')

    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(phone__icontains=query) |
            Q(workplace__icontains=query) |
            Q(position__icontains=query)
        )
    else:
        contacts = Contact.objects.none()

    return render(request, 'phonebook/search_results.html', {
        'contacts': contacts,
        'query': query
    })