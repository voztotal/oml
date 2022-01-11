const apiUrls = {
    'DashboardSupervision': '/api/v1/dashboard_supervision',
    'AuditSupervisor': '/api/v1/audit_supervisor',
    'CampaignAgents': (id_campaign) => `/api/v1/campaign/${id_campaign}/agents`,
    'ActiveAgents': '/api/v1/active_agents',
    'UpdateAgentsCampaign': '/api/v1/campaign/agents_update',
};
export default apiUrls;
