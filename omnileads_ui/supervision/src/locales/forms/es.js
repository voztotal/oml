export default {
    pause_set: {
        new: {
            name: 'Nombre del conjunto',
            configured_pauses: 'Pausas configuradas',
            enter_name: 'Ingresa el nombre'
        }
    },
    pause_setting: {
        enter_time: 'Ingresa el tiempo',
        infinite_time: 'Tiempo infinito'
    },
    call_disposition: {
        enter_name: 'Ingresa el nombre'
    },
    external_system: {
        enter_name: 'Ingresa el nombre'
    },
    form: {
        enter_name: 'Ingresa el nombre',
        enter_description: 'Ingresa la descripcion',
        new_field: 'Nuevo campo',
        options_list: 'Opciones para la lista',
        field: {
            type: {
                text: 'Texto',
                date: 'Fecha',
                list: 'Lista',
                text_box: 'Caja de texto'
            }
        },
        validations: {
            required_name: 'El nombre es requerido',
            required_description: 'La descripcion es requerida',
            not_empty_list: 'La lista no puede estar vacia',
            field_already_in_form: 'El campo ya existe en el formulario',
            option_already_in_list: 'La opcion ya esta en la lista',
            not_empty_form_field: 'Debe existir al menos un campo en el formulario'
        }
    },
    pause: {
        enter_name: 'Ingresa el nombre',
        edit_pause: 'Edita la pausa',
        new_pause: 'Nueva pausa'
    },
    inbound_route: {
        enter_name: 'Ingresa el nombre',
        enter_phone: 'Ingresa el DID',
        enter_caller_id: 'Ingresa el prefijo caller ID',
        edit_inbound_route: 'Edita la ruta entrante',
        new_inbound_route: 'Nueva ruta entrante',
        languages: {
            en: 'Inglés',
            es: 'Español'
        },
        destination_types: {
            campaign: 'Campaña entrante',
            validation_date: 'Validación de fecha/hora',
            ivr: 'IVR',
            hangup: 'HangUp',
            id_client: 'Identificador cliente',
            custom_dst: 'Destino personalizado'
        }
    },
    outbound_route: {
        enter_name: 'Ingresa el nombre',
        edit_outbound_route: 'Edita la ruta saliente',
        new_outbound_route: 'Nueva ruta saliente'
    }
};
