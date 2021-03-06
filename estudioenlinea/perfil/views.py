from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from emitidos.models import ComprobantesEmitidos
from recibidos.models import ComprobantesRecibidos
from contribuyente.models import Contribuyente, Notificaciones
from .forms import resumen_form
from django.contrib import messages
from .scripts import emitidos_anual, recibidos_anual, ultimos_movimientos
import pandas as pd
import datetime as dt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.

#perfil del cliente------------------

@login_required
def perfil(request):
    emitidos = None
    recibidos = None
    notificaciones = None

    if Contribuyente.objects.filter(Usuario=request.user.id).exists():
        cont = Contribuyente.objects.get(Usuario=request.user.id)
        if ComprobantesEmitidos.objects.filter(Contribuyente_id=cont.id).exists():
            emitidos = ComprobantesEmitidos.objects.filter(Contribuyente_id=cont.id).values()
        if ComprobantesRecibidos.objects.filter(Contribuyente_id=cont.id).exists():
            recibidos = ComprobantesRecibidos.objects.filter(Contribuyente_id=cont.id).values()
        if Notificaciones.objects.filter(Contribuyente_id=cont.id).exists():  
            notificaciones = Notificaciones.objects.filter(Contribuyente_id=cont.id).values()
        
        if notificaciones:
            notificaciones = list(notificaciones)
            if len(notificaciones)>10:
                notificaciones = notificaciones[:10] #solo 10 ultimas notificaciones para el perfil

        ultimos_mov = ultimos_movimientos(emitidos,recibidos)

        mensaje = "Bienvenido!"       

        contexto = {
                    'cont':cont,    
                    'contribuyente':request.user,
                    'emitidos':emitidos,
                    'mensaje':mensaje,
                    'ultimos_movimientos':ultimos_mov,
                    'notificaciones':notificaciones,
                    }

        return render(request,'perfil/perfil.html',context=contexto)
    else:
        mensaje = "Este usuario no posee un contribuyente asociado a su perfil"
        return render(request,'perfil/perfil.html',{'mensaje':mensaje})

@method_decorator(login_required, name='dispatch')
class NotificacionesDetailView(DetailView):
    model= Notificaciones
  
    def get_queryset(self):
        #queryset = super(Notificaciones, self).get_queryset()
        cont = Contribuyente.objects.get(Usuario=self.request.user.id)
        return Notificaciones.objects.filter(Contribuyente_id=cont)

@method_decorator(login_required, name='dispatch')
class NotificacionesListView(ListView):
    model= Notificaciones
  
    def get_queryset(self):
        #queryset = super(Notificaciones, self).get_queryset()
        cont = Contribuyente.objects.get(Usuario=self.request.user.id)
        return Notificaciones.objects.filter(Contribuyente_id=cont)   
    



#Herramientas del contador----------------

@staff_member_required
def resumen(request):
    form = resumen_form(request.POST)  
    if request.method == 'POST':
        if form.is_valid():
            contribuyente = request.POST.get('contribuyente')
            request.session['contribuyente'] = contribuyente
            return redirect('resumen_success')

    return render(request,'perfil/resumen.html',{'form':form})

@staff_member_required
def resumen_success(request):
    Nombre_cont = None
    desde = None
    hasta = None
    if 'contribuyente' in request.session:
        Nombre_cont = Contribuyente.objects.get(id=request.session['contribuyente']).Razon_Social
        if request.method == "POST": 
            
            if request.POST.get('fecha_desde'):
                desde = request.POST.get('fecha_desde')
            
            if request.POST.get('fecha_hasta'):
                hasta = request.POST.get('fecha_hasta')
            
            #reporte emitidos
            if request.POST.get("reporte") == "Emitidos":
                if ComprobantesEmitidos.objects.filter(Contribuyente_id=request.session['contribuyente']).exists():
                    tabla = ComprobantesEmitidos.objects.filter(Contribuyente_id=request.session['contribuyente'])
                    if desde:
                        tabla = tabla.filter(Fecha__gte=dt.date(int(desde[:4]),int(desde[5:7]),int(desde[8:10])))
                    if hasta:
                        tabla = tabla.filter(Fecha__lte=dt.date(int(hasta[:4]),int(hasta[5:7]),int(hasta[8:10])))
                    tabla = tabla.values()
                    if len(tabla)>0:
                        df_html, df_html_totales, grafico = emitidos_anual(tabla)
                    else:
                        messages.info(request,"No se encontraron registros de comprobantes emitidos en el periodo consultado")
                        df_html = None
                        df_html_totales = None
                        grafico = None
                    contexto = {
                        'desde':desde,
                        'hasta':hasta,
                        'cont':Nombre_cont,
                        'df_html':df_html,
                        'df_html_totales':df_html_totales, 
                        'grafico':grafico,
                        'titulo':"Reporte de Comprobantes Emitidos"
                    }
                    return render(request, 'perfil/resumen_success.html',context=contexto)
                else:
                    messages.info(request,"No se encontraron los registros consultados")
                    return render(request, 'perfil/resumen_success.html',{'cont':Nombre_cont})

            #reporte recibidos
            if request.POST.get("reporte") == "Recibidos":
                if ComprobantesRecibidos.objects.filter(Contribuyente_id=request.session['contribuyente']).exists():
                    tabla = ComprobantesRecibidos.objects.filter(Contribuyente_id=request.session['contribuyente'])
                    if desde:
                        tabla = tabla.filter(Fecha__gte=dt.date(int(desde[:4]),int(desde[5:7]),int(desde[8:10])))
                    if hasta:
                        tabla = tabla.filter(Fecha__lte=dt.date(int(hasta[:4]),int(hasta[5:7]),int(hasta[8:10])))
                    tabla = tabla.values()
                    if len(tabla)>0:
                        df_html, df_html_totales, grafico = recibidos_anual(tabla)
                    else:
                        messages.info(request,"No se encontraron registros de comprobantes recibidos en el periodo consultado")
                        df_html = None
                        df_html_totales = None
                        grafico = None
                    contexto = {
                        'desde':desde,
                        'hasta':hasta,
                        'cont':Nombre_cont,
                        'df_html':df_html,
                        'df_html_totales':df_html_totales, 
                        'grafico':grafico,
                        'titulo':"Reporte de Comprobantes Recibidos"
                    }
                    return render(request, 'perfil/resumen_success.html',context=contexto)
                else:
                    messages.info(request,"No se encontraron los registros consultados")
                    return render(request, 'perfil/resumen_success.html',{'cont':Nombre_cont})


    return render(request, 'perfil/resumen_success.html',{'cont':Nombre_cont})

