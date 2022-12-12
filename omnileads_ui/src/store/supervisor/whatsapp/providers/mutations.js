export default {
    initWhatsappProviders (state, providers) {
        state.supWhatsappProviders = providers;
    },
    initWhatsappProvider (state, provider = null) {
        if (provider) {
            state.supWhatsappProvider = {
                id: provider.id,
                nombre: provider.nombre,
                tipo_proveedor: provider.tipo_proveedor,
                identificador: provider.identificador,
                token_autorizacion: provider.token_autorizacion
            };
        } else {
            state.supWhatsappProvider = {
                id: null,
                nombre: '',
                tipo_proveedor: null,
                identificador: '',
                token_autorizacion: ''
            };
        }
    }
};
