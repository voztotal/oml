import Index from '@/views/supervisor/whatsapp/Index';
import ProviderRoutes from './provider_routes';

const BASE_URL = 'supervisor_whatsapp';

export default [
    {
        path: `/${BASE_URL}`,
        name: `${BASE_URL}`,
        component: Index
    },
    ...ProviderRoutes
];
