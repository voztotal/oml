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
                configuracion: {
                    appname: line.configuracion.appname,
                    appid: line.configuracion.appid,
                    destino: line.configuracion.destino,
                    tipo_de_destino: line.configuracion.tipo_de_destino
                },
                horario: line.horario,
                mensaje_bienvenida: line.mensaje_bienvenida,
                mensaje_despedida: line.mensaje_despedida,
                mensaje_fueradehora: line.mensaje_fueradehora
            };
        } else {
            state.supWhatsappLine = {
                id: null,
                nombre: '',
                proveedor: null,
                numero: '',
                configuracion: {
                    appname: '',
                    appid: '',
                    destino: null,
                    tipo_de_destino: 0
                },
                horario: null,
                mensaje_bienvenida: '',
                mensaje_despedida: '',
                mensaje_fueradehora: ''
            };
        }
    },
    initFormFlag (state, flag) {
        state.isFormToCreate = flag;
    },
    initWhatsappLineCampaigns (state, campaigns) {
        state.supWhatsappLineCampaigns = campaigns;
    }
};
