/* Copyright (C) 2018 Freetech Solutions

 This file is part of OMniLeads

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License version 3, as published by
 the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see http://www.gnu.org/licenses/.

*/

var PREFIJO_BLOQUEAR = 'id_bloquear_';
var PREFIJO_OCULTAR = 'id_ocultar_';
var PREFIJO_OBLIGATORIO = 'id_obligatorio_';


$(function() {
    $('[id^="' + PREFIJO_BLOQUEAR + '"').each(function() {
        InicializarCheckboxDeBloquear(this.id);
    });
});

function InicializarCheckboxDeBloquear(id_bloquear) {
    var id_ocultar = id_bloquear.replace(PREFIJO_BLOQUEAR, PREFIJO_OCULTAR);
    var id_obligatorio = id_bloquear.replace(PREFIJO_BLOQUEAR, PREFIJO_OBLIGATORIO);
    if ($('#' + id_ocultar).length > 0){
        [id_ocultar, id_bloquear, id_obligatorio].map(achicarClass);
        EstablecerEstadoDeCheckboxOcultar(id_bloquear, id_ocultar);
        EstablecerEstadoDeCheckboxObligatorio(id_bloquear, id_obligatorio);
        $('#' + id_bloquear).change(function() {
            EstablecerEstadoDeCheckboxOcultar(id_bloquear, id_ocultar);
            EstablecerEstadoDeCheckboxObligatorio(id_bloquear, id_obligatorio);
        });
        $('#' + id_ocultar).change(function() {
            EstablecerEstadoDeCheckboxObligatorio(id_bloquear, id_obligatorio);
        });
    }
    else {
        // Agrego un div extra para que queden alineados por nombre de campo.
        $('#' + id_bloquear).parent().after('<div class="col-md-6"></div>');
    }
}

function EstablecerEstadoDeCheckboxOcultar(id_bloquear, id_ocultar) {
    if ($('#' + id_bloquear).prop('checked')) {
        $('#' + id_ocultar).prop('disabled', false);
    }
    else {
        $('#' + id_ocultar).prop('disabled', true);
        $('#' + id_ocultar).prop('checked', false);
    }
}

function EstablecerEstadoDeCheckboxObligatorio(id_bloquear, id_obligatorio) {
    if ($('#' + id_bloquear).prop('checked')) {
        $('#' + id_obligatorio).prop('disabled', true);
        $('#' + id_obligatorio).prop('checked', false);
    }
    else {
        $('#' + id_obligatorio).prop('disabled', false);
    }
}

function achicarClass(id_object) {
    $('#' +id_object).parent('div').addClass('col-md-4');
    $('#' +id_object).parent('div').removeClass('col-md-6');

}