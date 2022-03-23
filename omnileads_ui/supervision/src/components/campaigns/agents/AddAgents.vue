<template>
  <div>
    <div class="p-field p-col-12 p-md-12 p-lg-12">
      <Dropdown
        v-model="selectedAgent"
        :options="agents"
        optionLabel="agent"
        :placeholder="$tc('select_a', 1, { field: $tc('agent', 1) })"
        :filter="true"
        v-bind:filterPlaceholder="$t('find_by', { field: $t('name') })"
      />
    </div>
    <div class="p-field p-col-12 p-md-4 p-lg-4">
      <Button
        type="button"
        class="p-button p-button-secondary"
        v-bind:label="$t('actions.add')"
        @click="addAgent"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { getToasConfig } from '@/helpers/sweet_alerts_helper.js';

export default {
    data () {
        return {
            selectedAgent: null,
            agents: []
        };
    },
    methods: {
        updateAgentsDisplay () {
            const agentsCampaignIds = this.agents_by_campaign.map(
                (agent) => agent.agent_id
            );
            const activeAgentsFilter = this.active_agents.filter(
                (agent) => !agentsCampaignIds.includes(agent.agent_id)
            );
            this.agents = activeAgentsFilter.map((agent) => {
                return {
                    agent: agent.agent_full_name,
                    value: agent.agent_id
                };
            });
        },
        addAgent () {
            if (this.selectedAgent) {
                var agentId = this.selectedAgent.value;
                if (
                    this.agents_by_campaign.find((agent) => agentId === agent.agent_id)
                ) {
                    this.$swal(
                        getToasConfig(
                            this.$t('sweet_alert.title.warning'),
                            this.$t('pages.add_agents_to_campaign.already_agent_in_campaign'),
                            this.$t('sweet_alert.icons.warning')
                        )
                    );
                } else {
                    var agent = this.active_agents.find(
                        (agent) => agentId === agent.agent_id
                    );
                    this.addAgentToCampaign(agent);
                    this.selectedAgent = null;
                    this.$swal(
                        getToasConfig(
                            this.$t('sweet_alert.title.success'),
                            this.$t('pages.add_agents_to_campaign.agent_added_success'),
                            this.$t('sweet_alert.icons.success')
                        )
                    );
                }
            } else {
                this.$swal(
                    getToasConfig(
                        this.$t('sweet_alert.title.warning'),
                        this.$t('pages.add_agents_to_campaign.not_select_type', {
                            type: this.$t('agent')
                        }),
                        this.$t('sweet_alert.icons.warning')
                    )
                );
            }
        },
        ...mapActions(['addAgentToCampaign'])
    },
    watch: {
        agents_by_campaign: {
            deep: true,
            handler () {
                this.updateAgentsDisplay();
            }
        },
        active_agents: {
            deep: true,
            handler () {
                this.updateAgentsDisplay();
            }
        }
    },
    computed: {
        ...mapGetters({
            agents_by_campaign: 'getAgentsByCampaign',
            active_agents: 'getActiveAgents'
        })
    }
};
</script>
