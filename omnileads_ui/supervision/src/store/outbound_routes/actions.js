/* eslint-disable no-unused-vars */
import OutboundRouteService from '@/services/outbound_route_service';
const service = new OutboundRouteService();

export default {
    async initOutboundRoutes ({ commit }) {
        const { status, outboundRoutes } = await service.list();
        commit('initOutboundRoutes', status === 'SUCCESS' ? outboundRoutes : []);
    },
    async initOutboundRouteDetail ({ commit }, id) {
        const { status, outboundRoute } = await service.detail(id);
        commit('initOutboundRouteDetail', status === 'SUCCESS' ? outboundRoute : {});
    },
    initOutboundRouteForm ({ commit }, data = null) {
        commit('initOutboundRouteForm', data);
    },
    async createOutboundRoute ({ commit }, data) {
        return await service.create(data);
    },
    async updateOutboundRoute ({ commit }, { id, data }) {
        return await service.update(id, data);
    },
    async deleteOutboundRoute ({ commit }, id) {
        return await service.delete(id);
    },
    async initOutboundRouteSipTrunks ({ commit }) {
        const { status, sipTrunks } = await service.sip_trunks();
        commit('initOutboundRouteSipTrunks', status === 'SUCCESS' ? sipTrunks : []);
    }
};
