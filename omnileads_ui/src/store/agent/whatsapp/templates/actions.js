/* eslint-disable no-unused-vars */
// import Service from '@/services/agent/whatsapp/template_service';
// const service = new Service();

export default {
    agtWhatsTemplatesInit ({ commit }) {
        const data = [
            {
                id: 5,
                nombre: 'Plantilla1',
                tipo: 0,
                configuracion: {
                    text: 'Hola Emi, que onda...asdfads',
                    type: 'text'
                }
            },
            {
                id: 6,
                nombre: 'Plantilla2',
                tipo: 0,
                configuracion: {
                    text: 'Hola Mundo',
                    type: 'text'
                }
            }
        ];
        commit('agtWhatsTemplatesInit', data);
    },
    agtWhatsTemplateSendMsg ({ commit }, template) {
        console.log('Send template message: ', template);
    }
};
