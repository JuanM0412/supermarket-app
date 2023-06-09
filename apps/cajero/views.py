from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *


def inicioCajero(request):
    return render(request, 'cajero/inicio_cajero.html')


def inicioClientes(request):
    return render(request, 'cajero/cliente/inicio_clientes.html')


def añadirClientes(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
        
    else:
        cliente_form = ClienteForm()
    
    return render(request, 'cajero/cliente/añadir_cliente.html', {'cliente_form': cliente_form})


def mostrarClientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cajero/cliente/resultados.html', {'clientes': clientes})


def editarCliente(request, cedula):
    cliente_form, error = None, None
    try:
        cliente = Cliente.objects.get(cedula = cedula)
        if request.method == 'GET':
            cliente_form = ClienteForm(instance = cliente)
        else:
            cliente_form = ClienteForm(request.POST, instance = cliente)
            if cliente_form.is_valid():
                cliente = cliente_form.save(commit = False)
                cliente.save()
                return redirect('cajero:mostrar_clientes')

    except ObjectDoesNotExist as e:
        error = f'No se ha encontrado un cliente con la cédula {cedula}.'

    return render(request, 'cajero/cliente/modificar.html', {'cliente_form': cliente_form, 'error': error})


def eliminarCliente(request, cedula):
    cliente = Cliente.objects.get(cedula = cedula)
    cliente.delete()
    return redirect('cajero:mostrar_clientes')


def registrarFactura(request):
    if request.method == 'POST':
        factura_form = FacturaForm(request.POST)
        if factura_form.is_valid():
            factura = factura_form.save()
            id_factura = factura.id
            return redirect('cajero:registrar_venta', id_factura)
        
    else:
        factura_form = FacturaForm()
    
    return render(request, 'cajero/venta/registrar_factura.html', {'factura_form': factura_form})


def registrarVenta(request, id_factura):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        if venta_form.is_valid():
            venta = venta_form.save(commit = False)
            factura = Factura.objects.get(pk = id_factura)
            venta.id_factura = factura 
            venta.save()
            return redirect('cajero:registrar_venta', id_factura)

    else:
        venta_form = VentaForm()
    
    return render(request, 'cajero/venta/registrar_venta.html', {'venta_form': venta_form})


def historicoVentas(request, cedula):
    facturas = Factura.objects.filter(cliente_cedula = cedula)
    return render(request, 'cajero/venta/historial.html', {'facturas': facturas})