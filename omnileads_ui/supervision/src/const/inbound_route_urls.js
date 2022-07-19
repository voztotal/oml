export default {
    InboundRouteList: '/api/v1/inbound_routes',
    InboundRouteCreate: '/api/v1/inbound_routes/create/',
    InboundRouteDetail: (id) => `/api/v1/inbound_routes/${id}`,
    InboundRouteDelete: (id) => `/api/v1/inbound_routes/${id}/delete`,
    InboundRouteUpdate: (id) => `/api/v1/inbound_routes/${id}/update/`,
    InboundRouteDestinationsByType: '/api/v1/inbound_routes/destinations_by_type'
};
