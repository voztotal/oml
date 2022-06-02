/* Copyright (C) 2018 Freetech Solutions

 This file is part of OMniLeads

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see http://www.gnu.org/licenses/.

*/

/* global Urls gettext */

// Adiciona tooltip sobre campo de id agente

let music_order = [];

$(function () {
    $('#music_list').sortable({
        update: function( event, ui ) {
            orderChange();
        }
    });
    $('#save_button').click(function () {saveNewOrder();});
});

function getOrder() {
    music_order = [];
    $('#music_list').children().each(function(){
        music_order.push($(this).attr('music-id'));
    });
}

function orderChange() {
    getOrder();
    enableSaveOrder();
}

function enableSaveOrder() {
    $('#save_button').attr('disabled', false);
}
function disableSaveOrder() {
    $('#save_button').attr('disabled', true);
}
    
function saveNewOrder(callback_ok, callback_error) {
    disableSaveOrder();
    let post_data = {
        'id': $('#playlist_id').val(),
        'order': music_order,
    };
    var URL = Urls.api_playlist_save_order();
    $.ajax({
        url: URL,
        type: 'POST',
        dataType: 'json',
        data: post_data,
        success: function(data){
            if (data['status'] == 'ERROR') {
                saveError(data);
            }
            else
                callback_ok(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            callback_error();
            console.log(gettext('Error al ejecutar => ') + textStatus + ' - ' + errorThrown);
        }
    });
}

function saveError(data) {
alert(data)
}

function saveOK() {
    disableSaveOrder();
}