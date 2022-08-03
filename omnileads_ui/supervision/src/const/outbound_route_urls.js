export default {
    OutboundRouteList: '/api/v1/outbound_routes',
    OutboundRouteCreate: '/api/v1/outbound_routes/create/',
    OutboundRouteDetail: (id) => `/api/v1/outbound_routes/${id}`,
    OutboundRouteDelete: (id) => `/api/v1/outbound_routes/${id}/delete`,
    OutboundRouteUpdate: (id) => `/api/v1/outbound_routes/${id}/update/`,
    OutboundRouteOrphanTrunks: (id) => `/api/v1/outbound_routes/${id}/orphan_trunks`,
    OutboundRouteSipTrunks: '/api/v1/outbound_routes/sip_trunks'
};
