import urls from '../const/outbound_route_urls';
import { HTTP, BaseService } from './base_service';

export default class OutboundRouteService extends BaseService {
    async list () {
        try {
            const resp = await fetch(urls.OutboundRouteList, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener las rutas salientes');
            return [];
        }
    }

    async create (data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data));
            const resp = await fetch(
                urls.OutboundRouteCreate,
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo crear la ruta saliente');
            return {};
        }
    }

    async update (id, data) {
        try {
            this.setPayload(HTTP.PUT, JSON.stringify(data));
            const resp = await fetch(
                urls.OutboundRouteUpdate(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo actualizar la ruta saliente');
            console.error(error);
            return {};
        }
    }

    async detail (id) {
        try {
            const resp = await fetch(
                urls.OutboundRouteDetail(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo obtener el detalle de la ruta saliente');
            return [];
        }
    }

    async delete (id) {
        try {
            this.setPayload(HTTP.DELETE);
            const resp = await fetch(
                urls.OutboundRouteDelete(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo eliminar la ruta saliente');
            console.error(error);
            return {};
        } finally {
            this.initPayload();
        }
    }

    async sip_trunks () {
        try {
            const resp = await fetch(urls.OutboundRouteSipTrunks, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener las troncales sip');
            return [];
        }
    }
}
