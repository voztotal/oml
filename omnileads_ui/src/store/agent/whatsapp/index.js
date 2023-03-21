import ConversationActions from './conversation/actions';
import ConversationMutations from './conversation/mutations';
import ConversationState from './conversation/state';
import MessageActions from './messages/actions';
import MessageMutations from './messages/mutations';
import MessageState from './messages/state';
import TemplateActions from './templates/actions';
import TemplateMutations from './templates/mutations';
import TemplateState from './templates/state';
import ManagementActions from './management/actions';
import ManagementMutations from './management/mutations';
import ManagementState from './management/state';

export const AgentWhatsappState = {
    ...ConversationState,
    ...MessageState,
    ...TemplateState,
    ...ManagementState
};

export const AgentWhatsappMutations = {
    ...ConversationMutations,
    ...MessageMutations,
    ...TemplateMutations,
    ...ManagementMutations
};

export const AgentWhatsappActions = {
    ...ConversationActions,
    ...MessageActions,
    ...TemplateActions,
    ...ManagementActions
};
