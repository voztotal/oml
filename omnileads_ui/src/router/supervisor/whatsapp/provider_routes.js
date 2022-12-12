import Index from '@/views/supervisor/whatsapp/providers/Index';
import New from '@/views/supervisor/whatsapp/providers/New';
import Edit from '@/views/supervisor/whatsapp/providers/Edit';

const base_url_name = 'supervisor_whatsapp';

export default [
    {
        path: `/${base_url_name}/providers`,
        name: `${base_url_name}_providers`,
        component: Index,
        children: [
            {
                path: 'new',
                name: `${base_url_name}_providers_new`,
                component: New
            },
            {
                path: ':id/update',
                name: `${base_url_name}_providers_update`,
                component: Edit
            }
        ]
    }
];


