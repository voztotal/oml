import Index from '@/views/supervisor/whatsapp/lines/Index';
import { WHATSAPP_URL_NAME } from '@/globals/supervisor/whatsapp';

export default [
    {
        path: `/${WHATSAPP_URL_NAME}_lines`,
        name: `${WHATSAPP_URL_NAME}_lines`,
        component: Index
    }
];
