# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import requests

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormView
)
from django.views.generic.detail import DetailView
from ominicontacto_app.models import (
    Contacto, Campana, CalificacionCliente, AgenteProfile, MetadataCliente,
    WombatLog
)
from ominicontacto_app.forms import (
    FormularioCRMForm, CalificacionClienteForm, FormularioCalificacionFormSet,
    FormularioNuevoContacto, FormularioVentaFormSet
)

import logging as logging_


logger = logging_.getLogger(__name__)


class CalificacionClienteCreateView(CreateView):
    """
    Muestra el detalle de contacto
    """
    template_name = 'formulario/calificacion_create_update.html'
    context_object_name = 'calificacion_cliente'
    model = CalificacionCliente
    form_class = FormularioNuevoContacto

    def get_object(self, queryset=None):
        return Contacto.objects.get(pk=self.kwargs['pk_contacto'])

    def get_initial(self):
        initial = super(CalificacionClienteCreateView, self).get_initial()
        contacto = Contacto.objects.get(pk=self.kwargs['pk_contacto'])
        base_datos = contacto.bd_contacto
        nombres = base_datos.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        for nombre, dato in zip(nombres, datos):
            initial.update({nombre: dato})
        return initial

    def get_form(self, form_class):
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        self.object = self.get_object()
        base_datos = self.object.bd_contacto
        metadata = base_datos.get_metadata()
        campos = metadata.nombres_de_columnas
        return form_class(campos=campos, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        agente = AgenteProfile.objects.get(pk=self.kwargs['id_agente'])
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(initial=[
            {'campana': campana.id,
             'contacto': self.object.id,
             'agente': agente.id}],
            form_kwargs={'calificacion_choice': calificaciones,
                         'gestion': campana.gestion}
        )
        url_wombat_agente = '/'.join([settings.OML_WOMBAT_URL,
                                      'api/calls/?op=attr&wombatid={0}&attr=id_agente&val={1}'])
        r = requests.post(
            url_wombat_agente.format(self.kwargs['wombat_id'],
                                     self.kwargs['id_agente']))
        return self.render_to_response(self.get_context_data(
            form=form, calificacion_form=calificacion_form))

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(CalificacionClienteCreateView, self).get_context_data(**kwargs)
        context['pk_campana'] = self.kwargs['pk_campana']
        context['pk_contacto'] = self.kwargs['pk_contacto']
        context['id_agente'] = self.kwargs['id_agente']
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(
            self.request.POST, form_kwargs={'calificacion_choice': calificaciones,
                         'gestion': campana.gestion},
        instance= self.object)

        if form.is_valid():
            if calificacion_form.is_valid():
                return self.form_valid(form, calificacion_form)
            else:
                return self.form_invalid(form, calificacion_form)
        else:
            return self.form_invalid(form, calificacion_form)

    def form_valid(self, form, calificacion_form):
        self.object_calificacion =calificacion_form.save(commit=False)
        cleaned_data_calificacion = calificacion_form.cleaned_data
        calificacion = cleaned_data_calificacion[0]['calificacion']
        url_wombat = '/'.join([settings.OML_WOMBAT_URL,
                               'api/calls/?op=extstatus&wombatid={0}&status={1}'
                               ])

        if calificacion is None:
            self.object_calificacion[0].es_venta = True
            self.object_calificacion[0].wombat_id = int(self.kwargs['wombat_id'])
            self.object_calificacion[0].save()
            r = requests.post(
                url_wombat.format(self.kwargs['wombat_id'], "venta"))
            wombat_log = WombatLog.objects.obtener_wombat_log_contacto(
                self.object_calificacion[0].contacto)
            if wombat_log.count() > 0:
                wombat_log = wombat_log[0]
            else:
                wombat_log = None
            if wombat_log:
                wombat_log.calificacion = "venta"
                wombat_log.save()
            return redirect(self.get_success_url())
        else:
            self.object_calificacion[0].es_venta = False
            self.object_calificacion[0].wombat_id = int(self.kwargs['wombat_id'])
            self.object_calificacion[0].save()
            r = requests.post(
                url_wombat.format(self.kwargs['wombat_id'],
                                  self.object_calificacion[0].calificacion.nombre))
            wombat_log = WombatLog.objects.obtener_wombat_log_contacto(
                self.object_calificacion[0].contacto)
            if wombat_log.count() > 0:
                wombat_log = wombat_log[0]
            else:
                wombat_log = None
            if wombat_log:
                wombat_log.calificacion = self.object_calificacion[0].calificacion.nombre
                wombat_log.save()
            message = 'Operación Exitosa!\
                        Se llevó a cabo con éxito la calificacion del cliente'
            messages.success(self.request, message)
            return HttpResponseRedirect(reverse('calificacion_formulario_update',
                                                kwargs={
                                                    "pk_campana": self.kwargs[
                                                        'pk_campana'],
                                                    "pk_contacto": self.kwargs[
                                                        'pk_contacto'],
                                                    "wombat_id": self.kwargs[
                                                        'wombat_id'],
                                                    "id_agente": self.kwargs[
                                                        'id_agente']}))

    def form_invalid(self, form, calificacion_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, calificacion_form=calificacion_form))


    def get_success_url(self):
        return reverse('formulario_venta',
                       kwargs={"pk_campana": self.kwargs['pk_campana'],
                               "pk_contacto": self.kwargs['pk_contacto'],
                               "id_agente": self.kwargs['id_agente']})


class CalificacionClienteUpdateView(UpdateView):
    """
    Muestra el detalle de contacto
    """
    template_name = 'formulario/calificacion_create_update.html'
    context_object_name = 'calificacion_cliente'
    model = CalificacionCliente
    form_class = FormularioNuevoContacto

    def dispatch(self, *args, **kwargs):
        try:
            contacto = Contacto.objects.get(pk=self.kwargs['pk_contacto'])
        except Contacto.DoesNotExist:
            return HttpResponseRedirect(reverse('formulario_buscar',
                                                kwargs={"pk_campana":
                                                self.kwargs['pk_campana']}))
        try:
            CalificacionCliente.objects.get(contacto=contacto)
        except CalificacionCliente.DoesNotExist:
            return HttpResponseRedirect(reverse('calificacion_formulario_create',
                kwargs={"pk_campana": self.kwargs['pk_campana'],
                        "pk_contacto": self.kwargs['pk_contacto'],
                        "id_agente": self.kwargs['id_agente'],
                        "wombat_id": self.kwargs['wombat_id'],
                        }))

        return super(CalificacionClienteUpdateView, self).dispatch(*args,
                                                                  **kwargs)

    def get(self, request, *args, **kwargs):
        agente = AgenteProfile.objects.get(pk=self.kwargs['id_agente'])
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(initial=[
            {'campana': campana.id,
             'contacto': self.object.id,
             'agente': agente.id}],
            form_kwargs={'calificacion_choice': calificaciones,
                         'gestion': campana.gestion},
            instance=self.object
        )
        url_wombat_agente = '/'.join([settings.OML_WOMBAT_URL,
                                      'api/calls/?op=attr&wombatid={0}&attr=id_agente&val={1}'])
        r = requests.post(
            url_wombat_agente.format(self.kwargs['wombat_id'],
                                     self.kwargs['id_agente']))
        return self.render_to_response(self.get_context_data(
            form=form, calificacion_form=calificacion_form))

    def get_initial(self):
        initial = super(CalificacionClienteUpdateView, self).get_initial()
        contacto = Contacto.objects.get(pk=self.kwargs['pk_contacto'])
        base_datos = contacto.bd_contacto
        nombres = base_datos.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        for nombre, dato in zip(nombres, datos):
            initial.update({nombre: dato})
        return initial

    def get_form(self, form_class):
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        calificaciones = campana.calificacion_campana.calificacion.all()
        self.object = self.get_object()
        base_datos = self.object.bd_contacto
        metadata = base_datos.get_metadata()
        campos = metadata.nombres_de_columnas
        return form_class(campos=campos, **self.get_form_kwargs())

    def get_object(self, queryset=None):
        return Contacto.objects.get(pk=self.kwargs['pk_contacto'])

    def get_context_data(self, **kwargs):
        context = super(CalificacionClienteUpdateView, self).get_context_data(**kwargs)
        context['pk_campana'] = self.kwargs['pk_campana']
        context['pk_contacto'] = self.kwargs['pk_contacto']
        context['id_agente'] = self.kwargs['id_agente']
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(
            self.request.POST, form_kwargs={'calificacion_choice': calificaciones,
                                            'gestion': campana.gestion},
            instance= self.object)

        if form.is_valid():
            if calificacion_form.is_valid():
                return self.form_valid(form, calificacion_form)
            else:
                return self.form_invalid(form, calificacion_form)
        else:
            return self.form_invalid(form, calificacion_form)


    def form_valid(self, form, calificacion_form):
        self.object_calificacion = calificacion_form.save(commit=False)

        if not self.object_calificacion:
            self.object_calificacion = calificacion_form.cleaned_data[0]['id']
        else:
            self.object_calificacion = self.object_calificacion[0]

        calificacion = calificacion_form.cleaned_data[0]['calificacion']
        url_wombat = '/'.join([settings.OML_WOMBAT_URL,
                               'api/calls/?op=extstatus&wombatid={0}&status={1}'
                               ])

        if calificacion is None:
            self.object_calificacion.es_venta = True
            self.object_calificacion.save()
           # calificacion_form.es_venta = True
            #calificacion_form.save()
            r = requests.post(
                url_wombat.format(self.kwargs['wombat_id'], "venta"))
            wombat_log = WombatLog.objects.obtener_wombat_log_contacto(
                self.object_calificacion.contacto)
            if wombat_log.count() > 0:
                wombat_log = wombat_log[0]
            else:
                wombat_log = None
            if wombat_log:
                wombat_log.calificacion = "venta"
                wombat_log.save()
            return redirect(self.get_success_url())

        else:
            self.object_calificacion.es_venta = False
            self.object_calificacion.save()
            r = requests.post(
                url_wombat.format(self.kwargs['wombat_id'],
                                  self.object_calificacion.calificacion.nombre))
            wombat_log = WombatLog.objects.obtener_wombat_log_contacto(
                self.object_calificacion.contacto)
            if wombat_log.count() > 0:
                wombat_log = wombat_log[0]
            else:
                wombat_log = None
            if wombat_log:
                wombat_log.calificacion = self.object_calificacion.calificacion.nombre
                wombat_log.save()
            message = 'Operación Exitosa!\
            Se llevó a cabo con éxito la calificacion del cliente'
            messages.success(self.request, message)
            return HttpResponseRedirect(
                reverse('calificacion_formulario_update',
                        kwargs={
                            "pk_campana": self.kwargs[
                                'pk_campana'],
                            "pk_contacto": self.kwargs[
                                'pk_contacto'],
                            "wombat_id": self.kwargs[
                                'wombat_id'],
                            "id_agente": self.kwargs[
                                'id_agente']}))

    def form_invalid(self, form, calificacion_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, calificacion_form=calificacion_form))

    def get_success_url(self):
        return reverse('formulario_venta',
                       kwargs={"pk_campana": self.kwargs['pk_campana'],
                               "pk_contacto": self.kwargs['pk_contacto'],
                               "id_agente": self.kwargs['id_agente']})


class FormularioCreateFormView(CreateView):
    template_name = 'formulario/formulario_create.html'
    model = MetadataCliente
    form_class = FormularioNuevoContacto

    def get_object(self, queryset=None):
        return Contacto.objects.get(pk=self.kwargs['pk_contacto'])

    def get_initial(self):
        initial = super(FormularioCreateFormView, self).get_initial()
        contacto = Contacto.objects.get(pk=self.kwargs['pk_contacto'])
        base_datos = contacto.bd_contacto
        nombres = base_datos.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        for nombre, dato in zip(nombres, datos):
            initial.update({nombre: dato})
        return initial

    def get_form(self, form_class):
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        self.object = self.get_object()
        base_datos = self.object.bd_contacto
        metadata = base_datos.get_metadata()
        campos = metadata.nombres_de_columnas
        return form_class(campos=campos, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        agente = AgenteProfile.objects.get(pk=self.kwargs['id_agente'])
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        venta_form = FormularioVentaFormSet(initial=[
            {'campana': campana.id,
             'contacto': self.object.id,
             'agente': agente.id}],
            form_kwargs={'campos':campana.formulario.campos.all()}
        )

        return self.render_to_response(self.get_context_data(
            form=form, venta_form=venta_form))

    def get_context_data(self, **kwargs):
        context = super(
            FormularioCreateFormView, self).get_context_data(**kwargs)

        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        context['pk_formulario'] = campana.formulario.pk
        contacto = Contacto.objects.get(pk=self.kwargs['pk_contacto'])
        bd_contacto = campana.bd_contacto
        nombres = bd_contacto.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        mas_datos = []
        for nombre, dato in zip(nombres, datos):
            mas_datos.append((nombre, dato))
        context['contacto'] = contacto
        context['mas_datos'] = mas_datos

        return context

    def form_valid(self, form, venta_form):
        self.object_venta = venta_form.save(commit=False)
        cleaned_data_venta = venta_form.cleaned_data[0]
        del cleaned_data_venta['agente']
        del cleaned_data_venta['campana']
        del cleaned_data_venta['contacto']
        del cleaned_data_venta['id']
        metadata = json.dumps(cleaned_data_venta)
        self.object_venta[0].metadata = metadata
        self.object_venta[0].save()
        message = 'Operación Exitosa!' \
                  'Se llevó a cabo con éxito el llenado del formulario del' \
                  ' cliente'
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse('formulario_detalle',
                                            kwargs={"pk": self.object_venta[0].pk}))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        venta_form = FormularioVentaFormSet(
            self.request.POST, form_kwargs={'campos':campana.formulario.campos.all()},
        instance=self.object)

        if form.is_valid():
            if venta_form.is_valid():
                return self.form_valid(form, venta_form)
            else:
                return self.form_invalid(form, venta_form)
        else:
            return self.form_invalid(form, venta_form)


    def form_invalid(self, form, venta_form):

        message = '<strong>Operación Errónea!</strong> \
                  Error en el formulario revise bien los datos llenados.'

        messages.add_message(
            self.request,
            messages.WARNING,
            message,
        )
        return self.render_to_response(self.get_context_data(
            form=form, venta_form=venta_form))

    def get_success_url(self):
        # reverse('formulario_detalle',
        #         kwargs={"pk": self.kwargs['pk_campana'],
        #                 "pk_contacto": self.kwargs['pk_contacto'],
        #                 "id_agente": self.kwargs['id_agente']
        #                 }
        #         )
        reverse('view_blanco')


class FormularioDetailView(DetailView):
    template_name = 'formulario/formulario_detalle.html'
    model = MetadataCliente

    def get_context_data(self, **kwargs):
        context = super(
            FormularioDetailView, self).get_context_data(**kwargs)
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk'])
        campana = Campana.objects.get(pk=metadata.campana.pk)
        contacto = Contacto.objects.get(pk=metadata.contacto.pk)
        bd_contacto = campana.bd_contacto
        nombres = bd_contacto.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        mas_datos = []
        for nombre, dato in zip(nombres, datos):
            mas_datos.append((nombre, dato))

        context['contacto'] = contacto
        context['mas_datos'] = mas_datos
        context['metadata'] = json.loads(metadata.metadata)

        return context


class FormularioUpdateFormView(UpdateView):
    template_name = 'formulario/formulario_create.html'
    model = MetadataCliente
    form_class = FormularioNuevoContacto

    def get_object(self, queryset=None):
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        return metadata.contacto

    def get_initial(self):
        initial = super(FormularioUpdateFormView, self).get_initial()
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        contacto = metadata.contacto
        base_datos = contacto.bd_contacto
        nombres = base_datos.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        for nombre, dato in zip(nombres, datos):
            initial.update({nombre: dato})
        return initial

    def get_form(self, form_class):
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        campana = metadata.campana
        self.object = self.get_object()
        base_datos = self.object.bd_contacto
        metadata = base_datos.get_metadata()
        campos = metadata.nombres_de_columnas
        return form_class(campos=campos, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(
            FormularioUpdateFormView, self).get_context_data(**kwargs)
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])

        context['pk_formulario'] = metadata.campana.formulario.pk

        bd_contacto = metadata.campana.bd_contacto
        nombres = bd_contacto.get_metadata().nombres_de_columnas[2:]
        datos = json.loads(metadata.contacto.datos)
        mas_datos = []
        for nombre, dato in zip(nombres, datos):
            mas_datos.append((nombre, dato))
        context['contacto'] = metadata.contacto
        context['mas_datos'] = mas_datos

        return context

    def get(self, request, *args, **kwargs):
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        initial = {
            'campana': metadata.campana.id,
            'contacto': self.object.id,
            'agente': metadata.agente.id
        }
        for clave, valor in json.loads(metadata.metadata).items():
            initial.update({clave: valor})
        venta_form = FormularioVentaFormSet(
            initial=[initial],
            form_kwargs={'campos': metadata.campana.formulario.campos.all()},
        )

        return self.render_to_response(self.get_context_data(
            form=form, venta_form=venta_form))

    def form_valid(self, form, venta_form):
        self.object_venta = venta_form.save(commit=False)
        metadata_cliente = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        cleaned_data_venta = venta_form.cleaned_data[0]
        del cleaned_data_venta['agente']
        del cleaned_data_venta['campana']
        del cleaned_data_venta['contacto']
        del cleaned_data_venta['id']
        metadata = json.dumps(cleaned_data_venta)
        metadata_cliente.metadata = metadata
        metadata_cliente.save()
        message = 'Operación Exitosa!' \
                  'Se llevó a cabo con éxito el llenado del formulario del' \
                  ' cliente'
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse('formulario_detalle',
                                            kwargs={"pk": metadata_cliente.pk}))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        metadata = MetadataCliente.objects.get(pk=self.kwargs['pk_metadata'])
        campana = metadata.campana
        venta_form = FormularioVentaFormSet(
            self.request.POST, form_kwargs={'campos':campana.formulario.campos.all()},
        instance=self.object)

        if form.is_valid():
            if venta_form.is_valid():
                return self.form_valid(form, venta_form)
            else:
                return self.form_invalid(form, venta_form)
        else:
            return self.form_invalid(form, venta_form)


    def form_invalid(self, form, venta_form):

        message = '<strong>Operación Errónea!</strong> \
                  Error en el formulario revise bien los datos llenados.'

        messages.add_message(
            self.request,
            messages.WARNING,
            message,
        )
        return self.render_to_response(self.get_context_data(
            form=form, venta_form=venta_form))

    def get_success_url(self):
        # reverse('formulario_detalle',
        #         kwargs={"pk": self.kwargs['pk_campana'],
        #                 "pk_contacto": self.kwargs['pk_contacto'],
        #                 "id_agente": self.kwargs['id_agente']
        #                 }
        #         )
        reverse('view_blanco')


class CalificacionUpdateView(UpdateView):

    template_name = 'formulario/calificacion_create_update.html'
    context_object_name = 'calificacion_cliente'
    model = CalificacionCliente
    form_class = FormularioNuevoContacto

    def get_form(self, form_class):
        campana = self.get_object().campana
        calificaciones = campana.calificacion_campana.calificacion.all()
        return form_class(calificacion_choice=calificaciones,
                          **self.get_form_kwargs())

    def get_initial(self):
        initial = super(CalificacionUpdateView, self).get_initial()
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        contacto = calificacion.contacto
        base_datos = contacto.bd_contacto
        nombres = base_datos.get_metadata().nombres_de_columnas[1:]
        datos = json.loads(contacto.datos)
        for nombre, dato in zip(nombres, datos):
            initial.update({nombre: dato})
        return initial

    def get_form(self, form_class):
        self.object = self.get_object()
        base_datos = self.object.bd_contacto
        metadata = base_datos.get_metadata()
        campos = metadata.nombres_de_columnas
        return form_class(campos=campos, **self.get_form_kwargs())

    def get_object(self, queryset=None):
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        return calificacion.contacto

    def get(self, request, *args, **kwargs):
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        agente = calificacion.agente
        campana = calificacion.campana
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(initial=[
            {'campana': campana.id,
             'contacto': self.object.id,
             'agente': agente.id}],
            form_kwargs={'calificacion_choice': calificaciones,
                         'gestion': campana.gestion},
            instance=self.object
        )

        return self.render_to_response(self.get_context_data(
            form=form, calificacion_form=calificacion_form))

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(CalificacionUpdateView, self).get_context_data(**kwargs)
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        context['pk_campana'] = calificacion.campana.pk
        context['pk_contacto'] = calificacion.contacto.pk
        context['id_agente'] = calificacion.agente.pk
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        campana = calificacion.campana
        calificaciones = campana.calificacion_campana.calificacion.all()
        calificacion_form = FormularioCalificacionFormSet(
            self.request.POST, form_kwargs={'calificacion_choice': calificaciones,
                                            'gestion': campana.gestion},
            instance= self.object)

        if form.is_valid():
            if calificacion_form.is_valid():
                return self.form_valid(form, calificacion_form)
            else:
                return self.form_invalid(form, calificacion_form)
        else:
            return self.form_invalid(form, calificacion_form)


    def form_valid(self, form, calificacion_form):
        self.object_calificacion = calificacion_form.save(commit=False)
        if not self.object_calificacion:
            self.object_calificacion = calificacion_form.cleaned_data[0]['id']
        else:
            self.object_calificacion = self.object_calificacion[0]
        calificacion = calificacion_form.cleaned_data[0]['calificacion']
        url_wombat = '/'.join([settings.OML_WOMBAT_URL,
                               'api/calls/?op=extstatus&wombatid={0}&status={1}'
                               ])

        if calificacion is None:
            self.object_calificacion.es_venta = True
            self.object_calificacion.save()
            r = requests.post(
                url_wombat.format(self.object_calificacion.wombat_id, "venta"))
            return redirect(self.get_success_url())

        else:
            self.object_calificacion.es_venta = False
            self.object_calificacion.save()
            r = requests.post(
                url_wombat.format(self.object_calificacion.wombat_id,
                                  self.object_calificacion.calificacion.nombre))
            message = 'Operación Exitosa!\
            Se llevó a cabo con éxito la calificacion del cliente'
            messages.success(self.request, message)
            return HttpResponseRedirect(reverse('reporte_agente_calificaciones',
                           kwargs={
                                   "pk_agente": self.object_calificacion.agente.pk}))

    def form_invalid(self, form, calificacion_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, calificacion_form=calificacion_form))

    def get_success_url(self):
        calificacion = CalificacionCliente.objects.get(pk=self.kwargs['pk_calificacion'])
        return reverse('formulario_venta',
                       kwargs={
                           "pk_campana": calificacion.campana.pk,
                            "pk_contacto": calificacion.contacto.pk,
                            "id_agente": calificacion.agente.pk})
