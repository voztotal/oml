import ProvidersActions from './providers/actions';
import ProvidersMutations from './providers/mutations';
import ProvidersState from './providers/state';
import LineActions from './lines/actions';
import LineMutations from './lines/mutations';
import LineState from './lines/state';

export const SupervisorWhatsappState = {
    ...ProvidersState,
    ...LineState
};

export const SupervisorWhatsappMutations = {
    ...ProvidersMutations,
    ...LineMutations
};

export const SupervisorWhatsappActions = {
    ...ProvidersActions,
    ...LineActions
};
