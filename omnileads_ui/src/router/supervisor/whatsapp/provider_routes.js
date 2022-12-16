import Index from '@/views/supervisor/whatsapp/providers/Index';
import New from '@/views/supervisor/whatsapp/providers/New';
import Edit from '@/views/supervisor/whatsapp/providers/Edit';
import { WHATSAPP_URL_NAME } from '@/globals/supervisor/whatsapp';

export default [
    {
        path: `/${WHATSAPP_URL_NAME}_providers.html`,
        name: `${WHATSAPP_URL_NAME}_providers`,
        component: Index
    },
    {
        path: `/${WHATSAPP_URL_NAME}_providers/new`,
        name: `${WHATSAPP_URL_NAME}_providers_new`,
        component: New
    },
    {
        path: `/${WHATSAPP_URL_NAME}_providers/:id/update`,
        name: `${WHATSAPP_URL_NAME}_providers_update`,
        component: Edit
    }
];
