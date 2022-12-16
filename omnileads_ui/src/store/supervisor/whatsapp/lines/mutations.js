export default {
    initWhatsappLines (state, lines) {
        state.supWhatsappLines = lines;
    },
    initWhatsappLine (state, line = null) {
        if (line) {
            state.supWhatsappLine = {
                id: line.id,
                nombre: line.nombre,
                proveedor: line.proveedor,
                numero: line.numero,
                identificador: line.identificador,
                es_verificado: line.es_verificado,
                token_validacion: line.token_validacion,
                destino: line.destino,
                // tipo_de_destino: line.tipo_de_destino,
                mensaje_bienvenida: line.mensaje_bienvenida,
                mensaje_despedida: line.mensaje_despedida
            };
        } else {
            state.supWhatsappLine = {
                id: null,
                nombre: '',
                proveedor: null,
                numero: '',
                identificador: '',
                es_verificado: false,
                token_validacion: '',
                destino: null,
                tipo_de_destino: null,
                mensaje_bienvenida: '',
                mensaje_despedida: ''
            };
        }
    }
};
