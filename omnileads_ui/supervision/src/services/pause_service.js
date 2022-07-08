import urls from '../const/pause_urls';
import { HTTP, BaseService } from './base_service';

export default class PauseService extends BaseService {
    async list () {
        try {
            const resp = await fetch(urls.PauseList, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener las pausas');
            return [];
        }
    }

    async create (data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data));
            const resp = await fetch(
                urls.PauseCreate,
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo crear el pausa');
            return {};
        }
    }

    async update (id, data) {
        try {
            this.setPayload(HTTP.PUT, JSON.stringify(data));
            const resp = await fetch(
                urls.PauseUpdate(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo actualizar el pausa');
            console.error(error);
            return {};
        }
    }

    async detail (id) {
        try {
            const resp = await fetch(
                urls.PauseDetail(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo obtener el detalle del pausa');
            return [];
        }
    }

    async delete (id) {
        try {
            this.setPayload(HTTP.DELETE);
            const resp = await fetch(
                urls.PauseDelete(id),
                this.payload
            );
            return await resp.json();
        } catch (error) {
            console.error('No se pudo eliminar el pausa');
            console.error(error);
            return {};
        } finally {
            this.initPayload();
        }
    }

    async reactivate (id) {
        try {
            this.setPayload(HTTP.PUT);
            const resp = await fetch(
                urls.PauseReactivate(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo reactivar el pausa');
            console.error(error);
            return {};
        }
    }
}
