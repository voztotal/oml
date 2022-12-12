import Index from '@/views/supervisor/forms/Index';
import ProviderRoutes from './provider_routes';

export default [
    {
        path: '/supervisor_forms.html',
        name: 'supervisor_forms',
        component: Index
    },
    ...ProviderRoutes
];
