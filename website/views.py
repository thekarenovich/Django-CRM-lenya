import io
from datetime import datetime

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.generic import View
from pyexcel_io import save_data
from xhtml2pdf import pisa

from .forms import SignUpForm, AddReagentForm
from .models import *


def export_reagent_to_pdf(request, pk):
    if request.user.is_authenticated:
        customer_reagent = Reagent.objects.get(id=pk)
        template_path = 'reagent_pdf_template.html'
        context = {'customer_reagent': customer_reagent}
        template = get_template(template_path)
        html = template.render(context)

        # Создаем PDF из HTML
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f'filename="reagent_{customer_reagent.reagent_name}_{customer_reagent.reagent_number}.pdf"'

        # Добавляем encoding='utf-8' для правильной обработки русских символов
        pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
        if pisa_status.err:
            return HttpResponse('Ошибка создания PDF: %s' % html)

        return response
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


class ExportExcelView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied

        reagents = Reagent.objects.all()

        data = {
            "Reagents": [
                ["Name & Number", "Container Number", "Quantity", "Type", "Created At", "Expiration Date",
                 "Storage Temperature", "Description", "Special Instructions", "Last Usage", "Last User", "ID"]
            ]
        }

        local_timezone = pytz.timezone('Europe/Moscow')  # Российское европейское время
        for reagent in reagents:
            created_at = datetime.combine(reagent.created_at, datetime.min.time()).astimezone(local_timezone).replace(
                tzinfo=None) if reagent.created_at else None
            expiration_date = datetime.combine(reagent.expiration_date, datetime.min.time()).astimezone(
                local_timezone).replace(tzinfo=None) if reagent.expiration_date else None
            last_usage = datetime.combine(reagent.last_usage, datetime.min.time()).astimezone(local_timezone).replace(
                tzinfo=None) if reagent.last_usage else None

            data["Reagents"].append([
                f"{reagent.reagent_name} {reagent.reagent_number}",
                reagent.container_number.container_number,
                reagent.quantity,
                reagent.reagent_type.name,
                created_at,
                expiration_date,
                reagent.storage_temperature,
                reagent.description,
                reagent.special_instructions,
                last_usage,
                reagent.last_user.username if reagent.last_user else "",
                reagent.id
            ])

        io_stream = io.BytesIO()
        save_data(io_stream, data, file_type='xlsx')
        io_stream.seek(0)

        response = HttpResponse(io_stream,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reagents.xlsx'
        return response


def storage_chamber(request, pk):
    if request.user.is_authenticated:
        chamber = Container.objects.get(id=pk).location.chamber
        return render(request, 'storage_chamber.html', {'chamber': chamber})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def storage_location(request, pk):
    if request.user.is_authenticated:
        location = Container.objects.get(id=pk).location
        return render(request, 'storage_location.html', {'location': location})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def container_number(request, pk):
    if request.user.is_authenticated:
        container = Container.objects.get(id=pk)
        return render(request, 'container_number.html', {'container': container})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def types(request):
    if request.user.is_authenticated:
        types = ReagentType.objects.all().order_by('code')
        return render(request, 'types.html', {'types': types})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def other_solution_type(request):
    if request.user.is_authenticated:
        other_solution = OtherSolution.objects.all()
        reagents = Reagent.objects.filter(reagent_type=1)
        return render(request, 'other_solution_type.html', {'other_solution': other_solution, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def buffer_solution_type(request):
    if request.user.is_authenticated:
        buffer_solution = BufferSolution.objects.all()
        reagents = Reagent.objects.filter(reagent_type=2)
        return render(request, 'buffer_solution_type.html', {'buffer_solution': buffer_solution, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def ferment_type(request):
    if request.user.is_authenticated:
        ferment_types = FermentType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=3)
        return render(request, 'ferment_type.html', {'ferment_types': ferment_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def dry_substance_type(request):
    if request.user.is_authenticated:
        dry_substance_types = DrySubstanceType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=4)
        return render(request, 'dry_substance_type.html', {'dry_substance_types': dry_substance_types,
                                                           'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def primer_type(request):
    if request.user.is_authenticated:
        primer_types = PrimerType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=5)
        return render(request, 'primer_type.html', {'primer_types': primer_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def restriction_enzyme_type(request):
    if request.user.is_authenticated:
        restriction_enzyme_types = RestrictionEnzymeType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=6)
        return render(request, 'restriction_enzyme_type.html',
                      {'restriction_enzyme_types': restriction_enzyme_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def substance_solution_type(request):
    if request.user.is_authenticated:
        substance_solution_types = SubstanceSolutionType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=7)
        return render(request, 'substance_solution_type.html',
                      {'substance_solution_types': substance_solution_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        reagents_list = Reagent.objects.all()

        sort_param = request.GET.get('sort')
        direction = request.GET.get('dir')

        if sort_param:
            if direction == 'asc':
                reagents_list = reagents_list.order_by(sort_param)
            elif direction == 'desc':
                reagents_list = reagents_list.order_by(F(sort_param).desc())

        paginator = Paginator(reagents_list, 3)
        page_number = request.GET.get('page')
        reagents = paginator.get_page(page_number)
        return render(request, 'home.html', {'reagents': reagents})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_reagent(request, pk):
    if request.user.is_authenticated:
        # Look Up reagents
        customer_reagent = Reagent.objects.get(id=pk)
        return render(request, 'reagent.html', {'customer_reagent': customer_reagent})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


def delete_reagent(request, pk):
    if request.user.is_authenticated:
        delete_it = Reagent.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Reagent Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')


def add_reagent(request):
    form = AddReagentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_reagent = form.save()
                messages.success(request, "Reagent Added...")
                return redirect('home')
        return render(request, 'add_reagent.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def update_reagent(request, pk):
    if request.user.is_authenticated:
        current_reagent = Reagent.objects.get(id=pk)
        form = AddReagentForm(request.POST or None, instance=current_reagent)
        if form.is_valid():
            form.save()
            messages.success(request, "Reagent Has Been Updated!")
            return redirect('home')
        return render(request, 'update_reagent.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
