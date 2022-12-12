import { BASE_URL_WHATSAPP } from './global_urls';

export default {
    List: `${BASE_URL_WHATSAPP}/providers`,
    Create: `${BASE_URL_WHATSAPP}/providers/create/`,
    Detail: (id) => `${BASE_URL_WHATSAPP}/providers/${id}`,
    Update: (id) => `${BASE_URL_WHATSAPP}/providers/${id}/update/`,
    Delete: (id) => `${BASE_URL_WHATSAPP}/providers/${id}/delete`
};