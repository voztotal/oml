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

$(function() {
   var start = moment();
   var end = moment();
   function cb(start, end) {
     $('#id_fecha').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
   }

   $('#id_fecha').on('apply.daterangepicker', function(ev, picker) {
     $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
   });

   $('#id_fecha').on('cancel.daterangepicker', function(ev, picker) {
     $(this).val('');
   });

   // Init daterange plugin
   var ranges = get_ranges();
   $('#id_fecha').daterangepicker(
     {
       locale: {
         format: 'DD/MM/YYYY'
       },
       startDate: start,
       endDate: end,
       ranges: ranges,
     }, cb);

   cb(start, end);

 });