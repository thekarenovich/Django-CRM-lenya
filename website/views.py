from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddReagentForm
from .models import *


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
    reagents = Reagent.objects.all()
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
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
