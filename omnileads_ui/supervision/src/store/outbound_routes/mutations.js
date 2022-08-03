export default {
    initOutboundRoutes (state, outboundRoutes) {
        state.outboundRoutes = outboundRoutes;
    },
    initOutboundRoute (state, outboundRoute) {
        if (outboundRoute === null) {
            state.outboundRoute = {
                id: null,
                nombre: '',
                ring_time: 25,
                dial_options: 'Tt',
                troncales: [],
                patrones_de_discado: []
            };
        } else {
            state.outboundRoute = {
                id: outboundRoute.id,
                nombre: outboundRoute.nombre,
                ring_time: outboundRoute.ring_time,
                dial_options: outboundRoute.dial_options,
                troncales: outboundRoute.troncales,
                patrones_de_discado: outboundRoute.patrones_de_discado
            };
        }
    },
    initOutboundRouteSipTrunks (state, sipTrunks) {
        state.sipTrunks = sipTrunks;
    },
    initOutboundRouteOrphanTrunks (state, orphanTrunks) {
        state.orphanTrunks = orphanTrunks;
    },
    initDialPatternForm (state, dialPattern) {
        if (dialPattern === null) {
            state.dialPattern = {
                id: null,
                prepend: null,
                prefix: null,
                match_pattern: null
            };
        } else {
            state.dialPattern = {
                id: dialPattern.id,
                prepend: dialPattern.prepend,
                prefix: dialPattern.prefix,
                match_pattern: dialPattern.match_pattern
            };
        }
    },
    addTrunk (state, trunk) {
        state.outboundRoute.troncales.push(trunk);
    },
    removeTrunk (state, trunkId) {
        state.outboundRoute.troncales = state.outboundRoute.troncales.filter(t => t.troncal !== trunkId);
    },
    addDialPattern (state, dialPattern) {
        state.outboundRoute.patrones_de_discado.push(dialPattern);
    },
    removeDialPattern (state, dialPattern) {
        if (dialPattern.id) {
            state.outboundRoute.patrones_de_discado = state.outboundRoute.patrones_de_discado.filter(pd => pd.id !== dialPattern.id);
        } else {
            state.outboundRoute.patrones_de_discado = state.outboundRoute.patrones_de_discado.filter(pd => pd.match_pattern !== dialPattern.match_pattern);
        }
    }
};
