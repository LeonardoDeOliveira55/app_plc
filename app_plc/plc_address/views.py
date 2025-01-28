from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Max, Min, Prefetch



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





###########################################################################################


class LocationListView(ListView):
    model = Location
    template_name = 'capacitors/location_list.html'
    context_object_name = 'locations'

class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'capacitors/location_form.html'
    success_url = reverse_lazy('location-list')

def configure_contactors(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    if request.method == 'POST':
        form = ContactorConfigForm(request.POST)
        if form.is_valid():
            num_contactors = form.cleaned_data['number_of_contactors']
            # Crear contactores
            for i in range(1, num_contactors + 1):
                Contactor.objects.create(location=location, number=i)
            return redirect('configure-capacitors', location_id=location.id)
    else:
        form = ContactorConfigForm()
    
    return render(request, 'capacitors/configure_contactors.html', {
        'location': location,
        'form': form
    })

def configure_capacitors(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    contactors = location.contactors.all()
    
    if request.method == 'POST':
        all_valid = True
        for contactor in contactors:
            # Limpia los capacitores existentes del contactor
            contactor.capacitors.all().delete()
            
            # Obtiene los valores KVAR seleccionados para este contactor
            kvar_values = request.POST.getlist(f'kvar_values_{contactor.id}')
            
            form_data = {
                'kvar_values': kvar_values
            }
            
            form = CapacitorConfigForm(
                form_data,
                kvar_choices=[(str(kv.id), str(kv)) for kv in KVARValue.objects.all()]
            )
            
            if form.is_valid():
                selected_values = form.cleaned_data['kvar_values']
                
                # Validar que no se excedan 3 baterías por contactor
                if len(selected_values) > 3:
                    messages.error(request, f'El contactor {contactor.number} no puede tener más de 3 baterías')
                    all_valid = False
                    continue
                
                # Crear capacitores para este contactor
                for i, kvar_id in enumerate(selected_values, 1):
                    Capacitor.objects.create(
                        contactor=contactor,
                        number=i,
                        kvar_value_id=int(kvar_id)
                    )
                contactor.is_configured = True
                contactor.save()
            else:
                all_valid = False
                messages.error(request, f'Error en el contactor {contactor.number}: {form.errors}')
        
        if all_valid:
            location.is_configured = True
            location.save()
            messages.success(request, 'Configuración guardada exitosamente')
            return redirect('location-detail', pk=location.id)
    
    # Preparar formularios para cada contactor
    forms = {
        contactor.id: CapacitorConfigForm(
            kvar_choices=[(str(kv.id), str(kv)) for kv in KVARValue.objects.all()]
        ) for contactor in contactors
    }
    
    return render(request, 'capacitors/configure_capacitors.html', {
        'location': location,
        'contactors': contactors,
        'forms': forms
    })

def measurement_form(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    contactors = location.contactors.all()
    
    if request.method == 'POST':
        all_valid = True
        measurements_created = []
        
        for contactor in contactors:
            form_data = {
                'current_r': request.POST.get(f'current_r_{contactor.id}'),
                'current_s': request.POST.get(f'current_s_{contactor.id}'),
                'current_t': request.POST.get(f'current_t_{contactor.id}'),
                'notes': request.POST.get(f'notes_{contactor.id}')
            }
            form = MeasurementForm(form_data)
            if form.is_valid():
                measurement = form.save(commit=False)
                measurement.contactor = contactor
                measurement.save()
                measurements_created.append(measurement)
            else:
                all_valid = False
                messages.error(request, f'Error en medición del contactor {contactor.number}')
        
        if all_valid:
            messages.success(request, "Mediciones guardadas correctamente")
            return redirect('measurement-results', location_id=location.id)
    
    # Preparar datos para el template
    contactor_data = []
    for contactor in contactors:
        expected_current = sum(cap.kvar_value.amperage for cap in contactor.capacitors.all())
        contactor_data.append({
            'contactor': contactor,
            'expected_current': expected_current,
            'form': MeasurementForm()
        })
    
    return render(request, 'capacitors/measurement_form.html', {
        'location': location,
        'contactor_data': contactor_data
    })

#def measurement_results(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    contactors = location.contactors.all().prefetch_related(
        'capacitors',
        'capacitors__kvar_value',
        'measurements'
    )

    # Preparar datos para la plantilla
    contactor_results = []
    for contactor in contactors:
        # Obtener la última medición
        last_measurement = contactor.measurements.last()
        
        if last_measurement:
            # Calcular la corriente nominal total esperada
            expected_current = sum(cap.kvar_value.amperage for cap in contactor.capacitors.all())
            
            # Calcular desviaciones
            deviation_r = ((last_measurement.current_r - expected_current) / expected_current) * 100
            deviation_s = ((last_measurement.current_s - expected_current) / expected_current) * 100
            deviation_t = ((last_measurement.current_t - expected_current) / expected_current) * 100

            # Determinar el estado de cada fase
            def get_status(deviation):
                if abs(deviation) <= 10:
                    return 'success', 'Normal'
                elif deviation > 10:
                    return 'danger', 'Alta corriente'
                else:
                    return 'danger', 'Baja corriente'

            status_r = get_status(deviation_r)
            status_s = get_status(deviation_s)
            status_t = get_status(deviation_t)

            contactor_results.append({
                'contactor': contactor,
                'capacitors': contactor.capacitors.all(),
                'measurement': last_measurement,
                'expected_current': expected_current,
                'deviation_r': deviation_r,
                'deviation_s': deviation_s,
                'deviation_t': deviation_t,
                'status_r': status_r,
                'status_s': status_s,
                'status_t': status_t,
                'measurement_date': last_measurement.measurement_date
            })

    return render(request, 'capacitors/measurement_results.html', {
        'location': location,
        'contactor_results': contactor_results
    })


def measurement_results(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    contactors = location.contactors.all().prefetch_related(
        'capacitors',
        'capacitors__kvar_value',
        'measurements'
    )

    # Preparar datos para la plantilla
    contactor_results = []
    for contactor in contactors:
        # Obtener la última medición
        last_measurement = contactor.measurements.last()
        
        if last_measurement:
            # Calcular la corriente nominal total esperada
            expected_current = sum(cap.kvar_value.amperage for cap in contactor.capacitors.all())
            
            # Corrientes medidas
            currents = [last_measurement.current_r, last_measurement.current_s, last_measurement.current_t]
            avg_current = sum(currents) / 3
            max_deviation = max(abs(c - avg_current) for c in currents)
            phase_unbalance = (max_deviation / avg_current) * 100 if avg_current > 0 else 0
            
            # Desviaciones individuales
            deviation_r = ((last_measurement.current_r - expected_current) / expected_current) * 100
            deviation_s = ((last_measurement.current_s - expected_current) / expected_current) * 100
            deviation_t = ((last_measurement.current_t - expected_current) / expected_current) * 100

            # Estado del desequilibrio
            unbalance_status = 'success' if phase_unbalance <= 10 else 'danger'
            unbalance_text = 'Normal' if phase_unbalance <= 10 else 'Desequilibrio'

            contactor_results.append({
                'contactor': contactor,
                'measurement': last_measurement,
                'expected_current': expected_current,
                'deviation_r': deviation_r,
                'deviation_s': deviation_s,
                'deviation_t': deviation_t,
                'phase_unbalance': phase_unbalance,
                'unbalance_status': unbalance_status,
                'unbalance_text': unbalance_text,
                'measurement_date': last_measurement.measurement_date
            })

    return render(request, 'capacitors/measurement_results.html', {
        'location': location,
        'contactor_results': contactor_results
    })

class LocationDetailView(DetailView):
    model = Location
    template_name = 'capacitors/location_detail.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.get_object()
        
        # Obtener todos los contactores ordenados por número
        contactors = location.contactors.all().order_by('number')
        
        # Para cada contactor, obtener su última medición
        for contactor in contactors:
            contactor.last_measurement = contactor.measurements.last()
            if contactor.last_measurement:
                # Calcular la corriente esperada
                expected_current = sum(cap.kvar_value.amperage for cap in contactor.capacitors.all())
                contactor.expected_current = expected_current
                
                # Calcular desviaciones
                contactor.deviation_r = ((contactor.last_measurement.current_r - expected_current) / expected_current) * 100
                contactor.deviation_s = ((contactor.last_measurement.current_s - expected_current) / expected_current) * 100
                contactor.deviation_t = ((contactor.last_measurement.current_t - expected_current) / expected_current) * 100
        
        context['contactors'] = contactors
        return context


#def measurement_history(request, location_id):
#    location = get_object_or_404(Location, id=location_id)
#    
#    # Obtener las fechas únicas de medición
#    measurement_dates = Measurement.objects.filter(
#        contactor__location=location
#    ).dates('measurement_date', 'day', order='DESC')
#    
#    measurements_by_date = {}
#    for date in measurement_dates:
#        # Obtener todas las mediciones de ese día
#        daily_measurements = Measurement.objects.filter(
#            contactor__location=location,
#            measurement_date__date=date
#        ).select_related(
#            'contactor',
#            'contactor__location'
#        ).prefetch_related(
#            'contactor__capacitors',
#            'contactor__capacitors__kvar_value'
#        ).order_by('contactor__number')
#
#        measurements_by_date[date] = []
#        for measurement in daily_measurements:
#            expected_current = sum(cap.kvar_value.amperage for cap in measurement.contactor.capacitors.all())
#            
#            # Calcular desviaciones
#            deviation_r = ((measurement.current_r - expected_current) / expected_current) * 100
#            deviation_s = ((measurement.current_s - expected_current) / expected_current) * 100
#            deviation_t = ((measurement.current_t - expected_current) / expected_current) * 100
#
#            measurements_by_date[date].append({
#                'measurement': measurement,
#                'expected_current': expected_current,
#                'deviation_r': deviation_r,
#                'deviation_s': deviation_s,
#                'deviation_t': deviation_t,
#            })

#    return render(request, 'capacitors/measurement_history.html', {
#        'location': location,
#        'measurements_by_date': measurements_by_date
#    })


def measurement_history(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    # Obtener las fechas únicas de medición
    measurement_dates = Measurement.objects.filter(
        contactor__location=location
    ).dates('measurement_date', 'day', order='DESC')
    
    measurements_by_date = {}
    for date in measurement_dates:
        daily_measurements = Measurement.objects.filter(
            contactor__location=location,
            measurement_date__date=date
        ).select_related(
            'contactor',
            'contactor__location'
        ).prefetch_related(
            'contactor__capacitors',
            'contactor__capacitors__kvar_value'
        ).order_by('contactor__number')

        measurements_by_date[date] = []
        for measurement in daily_measurements:
            expected_current = sum(cap.kvar_value.amperage for cap in measurement.contactor.capacitors.all())
            
            # Calcular desequilibrio entre fases
            currents = [measurement.current_r, measurement.current_s, measurement.current_t]
            avg_current = sum(currents) / 3
            max_deviation = max(abs(c - avg_current) for c in currents)
            phase_unbalance = (max_deviation / avg_current) * 100 if avg_current > 0 else 0

            measurements_by_date[date].append({
                'measurement': measurement,
                'expected_current': expected_current,
                'phase_unbalance': phase_unbalance,
                'unbalance_status': 'success' if phase_unbalance <= 10 else 'danger',
                'deviation_r': ((measurement.current_r - expected_current) / expected_current) * 100,
                'deviation_s': ((measurement.current_s - expected_current) / expected_current) * 100,
                'deviation_t': ((measurement.current_t - expected_current) / expected_current) * 100,
            })

    return render(request, 'capacitors/measurement_history.html', {
        'location': location,
        'measurements_by_date': measurements_by_date
    })