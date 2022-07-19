import urls from '../const/inbound_route_urls';
import { HTTP, BaseService } from './base_service';

export default class InboundRouteService extends BaseService {
    async list () {
        try {
            const resp = await fetch(urls.InboundRouteList, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener las rutas entrantes');
            return [];
        }
    }

    async create (data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data));
            const resp = await fetch(
                urls.InboundRouteCreate,
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo crear la ruta entrante');
            return {};
        }
    }

    async update (id, data) {
        try {
            this.setPayload(HTTP.PUT, JSON.stringify(data));
            const resp = await fetch(
                urls.InboundRouteUpdate(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo actualizar la ruta entrante');
            console.error(error);
            return {};
        }
    }

    async detail (id) {
        try {
            const resp = await fetch(
                urls.InboundRouteDetail(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo obtener el detalle de la ruta entrante');
            return [];
        }
    }

    async delete (id) {
        try {
            this.setPayload(HTTP.DELETE);
            const resp = await fetch(
                urls.InboundRouteDelete(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo eliminar la ruta entrante');
            console.error(error);
            return {};
        } finally {
            this.initPayload();
        }
    }

    async destinations () {
        try {
            const resp = await fetch(urls.InboundRouteDestinationsByType, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener los destinos');
            return [];
        }
    }
}
