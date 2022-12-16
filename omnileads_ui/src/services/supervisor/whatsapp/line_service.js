import urls from '@/api_urls/supervisor/whatsapp/line_urls';
import { BaseService } from '@/services/base_service';

export default class LineService extends BaseService {
    constructor () {
        super(urls, 'Linea de WhatsApp');
    }
}
