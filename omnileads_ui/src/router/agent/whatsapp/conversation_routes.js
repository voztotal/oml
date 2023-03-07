import Index from '@/views/agent/whatsapp/conversation/Index';
import { WHATSAPP_URL_NAME } from '@/globals/agent/whatsapp';

export default [
    {
        path: `/${WHATSAPP_URL_NAME}_conversation.html`,
        name: `${WHATSAPP_URL_NAME}_conversation`,
        component: Index
    }
];
