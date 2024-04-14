import io

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

from .forms import SignUpForm, AddReagentForm, MagazineForm
from .models import *


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
        page_obj = paginator.get_page(page_number)
        return render(request, 'home.html', {'page_obj': page_obj})


def get_magazines(request):
    if request.user.is_authenticated:
        magazines_list = Magazine.objects.all()
        paginator = Paginator(magazines_list, 3)  # Разбиваем на страницы по 3 элемента на каждой
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'get_magazines.html', {'page_obj': page_obj})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


def add_magazine(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MagazineForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = MagazineForm()
        return render(request, 'add_magazine.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


def export_reagent_to_pdf(request, pk):
    if request.user.is_authenticated:
        customer_reagent = Reagent.objects.get(id=pk)
        template_path = 'reagent_pdf_template.html'
        context = {'customer_reagent': customer_reagent}
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f'filename="reagent_{customer_reagent.reagent_name}_{customer_reagent.reagent_number}.pdf"'
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

        local_timezone = pytz.timezone('Europe/Moscow')
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


def storage_chamber(request, container_number):
    if request.user.is_authenticated:
        chamber = Container.objects.get(container_number=container_number).location.chamber
        return render(request, 'storage_chamber.html', {'chamber': chamber})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def storage_location(request, container_number):
    if request.user.is_authenticated:
        location = Container.objects.get(container_number=container_number)
        return render(request, 'storage_location.html', {'location': location})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def container_number(request, container_number):
    if request.user.is_authenticated:
        container = Container.objects.get(container_number=container_number)
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
        reagents = Reagent.objects.filter(reagent_type=4)
        return render(request, 'other_solution_type.html', {'other_solution': other_solution, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def buffer_solution_type(request):
    if request.user.is_authenticated:
        buffer_solution = BufferSolution.objects.all()
        reagents = Reagent.objects.filter(reagent_type=3)
        return render(request, 'buffer_solution_type.html', {'buffer_solution': buffer_solution, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def ferment_type(request):
    if request.user.is_authenticated:
        ferment_types = FermentType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=6)
        return render(request, 'ferment_type.html', {'ferment_types': ferment_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def dry_substance_type(request):
    if request.user.is_authenticated:
        dry_substance_types = DrySubstanceType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=1)
        return render(request, 'dry_substance_type.html', {'dry_substance_types': dry_substance_types,
                                                           'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def primer_type(request):
    if request.user.is_authenticated:
        primer_types = PrimerType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=7)
        return render(request, 'primer_type.html', {'primer_types': primer_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def restriction_enzyme_type(request):
    if request.user.is_authenticated:
        restriction_enzyme_types = RestrictionEnzymeType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=5)
        return render(request, 'restriction_enzyme_type.html',
                      {'restriction_enzyme_types': restriction_enzyme_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def substance_solution_type(request):
    if request.user.is_authenticated:
        substance_solution_types = SubstanceSolutionType.objects.all()
        reagents = Reagent.objects.filter(reagent_type=2)
        return render(request, 'substance_solution_type.html',
                      {'substance_solution_types': substance_solution_types, 'reagents': reagents})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
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


##################################
##################################
#                                #
# Repository (operations for db) #
#                                #
##################################
##################################
def add_container_type(request):
    values_to_add = [
        "Бутылка стеклянная",
        "Бутылка пластиковая",
        "Фалькон",
        "Пробирка стеклянная",
        "Стрип",
        "Плашка",
        "Колба стеклянная",
        "Чашка петри",
        "Пробирка центрифужная 1.5",
        "Пробирка центрифужная 0.6",
        "Пробирка центрифужная 0.2",
    ]
    for value in values_to_add:
        container_type = ContainerType.objects.create(name=value)
        print(f"Добавлено: {container_type}")
    return redirect('home')


def add_reagent_type(request):
    values_to_add = [
        "Сухое вещество",
        "Раствор вещества",
        "Буферный раствор",
        "Другой раствор",
        "Рестриктаза",
        "Фермент",
        "Праймер",
    ]
    for value in values_to_add:
        reagent_type = ReagentType.objects.create(name=value)
        print(f"Добавлено: {reagent_type}")
    return redirect('home')


def add_storage_chamber(request):
    data_to_add = [
        {"name": "Камера 1", "shelf_number": 5},
        {"name": "Камера 2", "shelf_number": 3},
    ]
    for data in data_to_add:
        storage_chamber = StorageChamber.objects.create(
            name=data["name"],
            shelf_number=data["shelf_number"]
        )
        print(f"Добавлено: {storage_chamber}")
    return redirect('home')


def add_storage_location(request):
    storage_chamber = StorageChamber.objects.get(pk=1)
    data_to_add = [
        {"name": "Место 1"},
        {"name": "Место 2"},
    ]
    for data in data_to_add:
        storage_location = StorageLocation.objects.create(
            name=data["name"],
            chamber=storage_chamber
        )
        print(f"Добавлено: {storage_location}")
    return redirect('home')


def add_container(request):
    storage_location = StorageLocation.objects.get(pk=1)
    container_type = ContainerType.objects.get(pk=1)
    data_to_add = [
        {"container_number": "1234", "reagent_quantity": 100},
        {"container_number": "5678", "reagent_quantity": 200},
    ]
    for data in data_to_add:
        container = Container.objects.create(
            container_number=data["container_number"],
            location=storage_location,
            container_type=container_type,
            reagent_quantity=data["reagent_quantity"]
        )
        print(f"Добавлено: {container}")
    return redirect('home')


def add_other_solutions(request):
    reagent_type_other = ReagentType.objects.get(name="Другой раствор")
    data_to_add = [
        {"reagent": 123, "component_concentration": 1.5, "molarity": 0.1, "ph": 7.0},
    ]
    for data in data_to_add:
        other_solution = OtherSolution.objects.create(
            reagent=data["reagent"],
            component_concentration=data["component_concentration"],
            molarity=data["molarity"],
            ph=data["ph"],
            reagent_type=reagent_type_other
        )
        print(f"Добавлено: {other_solution}")
    return redirect('home')


def add_buffer_solutions(request):
    reagent_type_buffer = ReagentType.objects.get(name="Буферный раствор")
    data_to_add = [
        {"reagent": 789, "component_concentration": 1.0, "molarity": 0.05, "ph": 8.0},
    ]
    for data in data_to_add:
        buffer_solution = BufferSolution.objects.create(
            reagent=data["reagent"],
            component_concentration=data["component_concentration"],
            molarity=data["molarity"],
            ph=data["ph"],
            reagent_type=reagent_type_buffer
        )
        print(f"Добавлено: {buffer_solution}")
    return redirect('home')


def add_ferment_types(request):
    reagent_type_ferment = ReagentType.objects.get(name="Фермент")
    data_to_add = [
        {"reagent": 1315, "class_name": "Тип 1", "activity_per_ml": 10, "optimal_temperature": 37,
         "deactivation_capability": "Высокая", "storage_buffer_type": "Трис-солевый", "reaction_buffer": "PBS",
         "source": "Естественный источник"},
    ]
    for data in data_to_add:
        ferment_type = FermentType.objects.create(
            reagent=data["reagent"],
            class_name=data["class_name"],
            activity_per_ml=data["activity_per_ml"],
            optimal_temperature=data["optimal_temperature"],
            deactivation_capability=data["deactivation_capability"],
            storage_buffer_type=data["storage_buffer_type"],
            reaction_buffer=data["reaction_buffer"],
            source=data["source"],
            reagent_type=reagent_type_ferment
        )
        print(f"Добавлено: {ferment_type}")
    return redirect('home')


def add_dry_substance_types(request):
    reagent_type_dry_substance = ReagentType.objects.get(name="Сухое вещество")
    data_to_add = [
        {"reagent": 2022, "supplier": "Компания А", "purity": 99.5, "applications": "Исследования в области биохимии"},
    ]
    for data in data_to_add:
        dry_substance_type = DrySubstanceType.objects.create(
            reagent=data["reagent"],
            supplier=data["supplier"],
            purity=data["purity"],
            applications=data["applications"],
            reagent_type=reagent_type_dry_substance
        )
        print(f"Добавлено: {dry_substance_type}")
    return redirect('home')


def add_primer_types(request):
    reagent_type_primer = ReagentType.objects.get(name="Праймер")
    data_to_add = [
        {"reagent": 4044, "sequence": "ATCGATCGATCG", "annealing_temperature": 60,
         "composition_for_annealing_temperature": "Солевой буфер", "concentration": 100, "length": 20},
    ]
    for data in data_to_add:
        primer_type = PrimerType.objects.create(
            reagent=data["reagent"],
            sequence=data["sequence"],
            annealing_temperature=data["annealing_temperature"],
            composition_for_annealing_temperature=data["composition_for_annealing_temperature"],
            concentration=data["concentration"],
            length=data["length"],
            reagent_type=reagent_type_primer
        )
        print(f"Добавлено: {primer_type}")
    return redirect('home')


def add_restriction_enzyme_types(request):
    reagent_type_restriction_enzyme = ReagentType.objects.get(name="Рестриктаза")
    data_to_add = [
        {"reagent": 6066, "activity_percentage_in_buffers": 90, "activity_per_ml": 5000, "optimal_temperature": 37,
         "deactivation_capability": "Низкая", "storage_buffer_type": "Трис-солевый", "reaction_buffer": "EcoRI",
         "restriction_site": "GAATTC"},
    ]
    for data in data_to_add:
        restriction_enzyme_type = RestrictionEnzymeType.objects.create(
            reagent=data["reagent"],
            activity_percentage_in_buffers=data["activity_percentage_in_buffers"],
            activity_per_ml=data["activity_per_ml"],
            optimal_temperature=data["optimal_temperature"],
            deactivation_capability=data["deactivation_capability"],
            storage_buffer_type=data["storage_buffer_type"],
            reaction_buffer=data["reaction_buffer"],
            restriction_site=data["restriction_site"],
            reagent_type=reagent_type_restriction_enzyme
        )
        print(f"Добавлено: {restriction_enzyme_type}")
    return redirect('home')


def add_substance_solution_types(request):
    reagent_type_substance_solution = ReagentType.objects.get(name="Раствор вещества")
    data_to_add = [
        {"reagent": 8088, "dry_reagent": "Сахароза", "dry_reagent_quantity": 50, "concentration": 10,
         "solvent": "Вода"},
    ]
    for data in data_to_add:
        substance_solution_type = SubstanceSolutionType.objects.create(
            reagent=data["reagent"],
            dry_reagent=data["dry_reagent"],
            dry_reagent_quantity=data["dry_reagent_quantity"],
            concentration=data["concentration"],
            solvent=data["solvent"],
            reagent_type=reagent_type_substance_solution
        )
        print(f"Добавлено: {substance_solution_type}")
    return redirect('home')


from datetime import datetime, timedelta


def add_reagents(request):
    container_number = Container.objects.get(container_number="1234")
    reagent_type = ReagentType.objects.get(name="Рестриктаза")
    user = User.objects.get(username="thekarenovich")

    data_to_add = [
        {"reagent_number": 99, "reagent_name": "Реагент 1", "quantity": 50,
         "expiration_date": datetime.now() + timedelta(days=365), "storage_temperature": 4,
         "description": "Описание реагента 1", "special_instructions": "Особые указания реагента 1"},
        {"reagent_number": 88, "reagent_name": "Реагент 2", "quantity": 100,
         "expiration_date": datetime.now() + timedelta(days=365), "storage_temperature": 4,
         "description": "Описание реагента 2", "special_instructions": "Особые указания реагента 2"},
        {"reagent_number": 77, "reagent_name": "Реагент 3", "quantity": 200,
         "expiration_date": datetime.now() + timedelta(days=365), "storage_temperature": 4,
         "description": "Описание реагента 3", "special_instructions": "Особые указания реагента 3"},
    ]

    for data in data_to_add:
        reagent = Reagent.objects.create(
            reagent_number=data["reagent_number"],
            reagent_name=data["reagent_name"],
            container_number=container_number,
            quantity=data["quantity"],
            reagent_type=reagent_type,
            created_at=datetime.now(),
            expiration_date=data["expiration_date"],
            storage_temperature=data["storage_temperature"],
            description=data["description"],
            special_instructions=data["special_instructions"],
            last_user=user,
        )
        print(f"Добавлено: {reagent}")

    return redirect('home')
