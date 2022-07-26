export default {
    initOutboundRoutes (state, outboundRoutes) {
        state.outboundRoutes = outboundRoutes;
    },
    initOutboundRoutesDestinations (state, destinations) {
        state.destinations = destinations;
    },
    initOutboundRouteDetail (state, outboundRoute) {
        state.outboundRouteDetail = outboundRoute;
    },
    initOutboundRouteForm (state, outboundRoute) {
        if (outboundRoute === null) {
            state.outboundRouteForm = {
                id: null
            };
        } else {
            state.outboundRouteForm = {
                id: outboundRoute.id
            };
        }
    }
};
