import Index from '@/views/agent/whatsapp/management_form/Index';
import { WHATSAPP_URL_NAME } from '@/globals/agent/whatsapp';

export default [
    {
        path: `/${WHATSAPP_URL_NAME}_management_form`,
        name: `${WHATSAPP_URL_NAME}_management_form`,
        component: Index
    }
];
