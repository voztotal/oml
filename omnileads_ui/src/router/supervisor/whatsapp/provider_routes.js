import Index from '@/views/supervisor/whatsapp/providers/Index';
import New from '@/views/supervisor/whatsapp/providers/New';
import Edit from '@/views/supervisor/whatsapp/providers/Edit';

const BASE_URL = 'supervisor_whatsapp';

export default [
    {
        path: `/${BASE_URL}/providers`,
        name: `${BASE_URL}_providers`,
        component: Index
    },
    {
        path: `/${BASE_URL}/providers/new`,
        name: `${BASE_URL}_providers_new`,
        component: New
    },
    {
        path: `/${BASE_URL}/providers/:id/update`,
        name: `${BASE_URL}_providers_update`,
        component: Edit
    }
];
