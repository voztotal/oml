import Index from '@/views/agent/whatsapp/conversation/Index';
import MediaUploader from '@/views/agent/whatsapp/conversation/MediaUploader';
import { WHATSAPP_URL_NAME } from '@/globals/agent/whatsapp';

export default [
    {
        path: `/${WHATSAPP_URL_NAME}_conversation/:id`,
        name: `${WHATSAPP_URL_NAME}_conversation_detail`,
        component: Index
    },
    {
        path: `/${WHATSAPP_URL_NAME}_media_uploader.html`,
        name: `${WHATSAPP_URL_NAME}_media_uploader`,
        component: MediaUploader
    }
];
