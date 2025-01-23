from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, UpdateView
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


@login_required
def home(request):
    search_query = request.GET.get('search', '')
    tags = Tag.objects.all()
    
    if search_query:
        tags = tags.filter(nombre__icontains=search_query)
    
    return render(request, 'plc_crud/home.html', {
        'tags': tags,
        'search_query': search_query
    })



@login_required
def tag_detail(request, pk):
    tag = Tag.objects.get(pk=pk)
    direcciones = tag.direcciones.all()
    form = DireccionForm()
    
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.tag = tag
            direccion.save()
            return redirect('tag_detail', pk=pk)
            
    return render(request, 'plc_crud/tag_detail.html', {
        'tag': tag,
        'direcciones': direcciones,
        'form': form
    })

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'plc_crud/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'plc_crud/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('login')

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'plc_crud/edit_user.html', {'form': form})

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'plc_crud/tag_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Tag creado exitosamente!')
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'plc_crud/tag_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # Asegura que el usuario solo pueda editar sus propios tags
        return Tag.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tag actualizado exitosamente!')
        return super().form_valid(form)
    

@login_required
def eliminar_direccion(request, tag_id, direccion_id):
    try:
        direccion = Direccion.objects.get(id=direccion_id, tag_id=tag_id, tag__usuario=request.user)
        direccion.delete()
        messages.success(request, 'Dirección eliminada exitosamente')
    except Direccion.DoesNotExist:
        messages.error(request, 'La dirección no existe o no tienes permiso para eliminarla')
    
    return redirect('tag_detail', pk=tag_id)

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag eliminado exitosamente')
        return redirect('home')

    return redirect('home')


def obtener_sectores(request, empresa_id):
    sectores = list(Sector.objects.filter(empresa_id=empresa_id).values('id', 'sector', 'ubicacion'))
    return JsonResponse(sectores, safe=False)


@login_required
def empresa_list(request):
    empresas = Empresa.objects.all()
    return render(request, 'plc_crud/empresa_list.html', {'empresas': empresas})

@login_required
def empresa_create(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa creada exitosamente!')
            return redirect('empresa_list')
    else:
        form = EmpresaForm()
    return render(request, 'plc_crud/empresa_form.html', {'form': form})

@login_required
def empresa_edit(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa actualizada exitosamente!')
            return redirect('empresa_list')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'plc_crud/empresa_form.html', {'form': form, 'empresa': empresa})

@login_required
def empresa_delete(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente!')
    return redirect('empresa_list')

@login_required
def sector_list(request):
    sectores = Sector.objects.all()
    return render(request, 'plc_crud/sector_list.html', {'sectores': sectores})

@login_required
def sector_create(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ubicación creada exitosamente!')
            return redirect('sector_list')
    else:
        form = SectorForm()
    return render(request, 'plc_crud/sector_form.html', {'form': form})

@login_required
def sector_edit(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    if request.method == "POST":
        form = SectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ubicación actualizada exitosamente!')
            return redirect('sector_list')
    else:
        form = SectorForm(instance=sector)
    return render(request, 'plc_crud/sector_form.html', {'form': form, 'sector': sector})

@login_required
def sector_delete(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    if request.method == "POST":
        sector.delete()
        messages.success(request, 'Ubicación eliminada exitosamente!')
    return redirect('sector_list')
