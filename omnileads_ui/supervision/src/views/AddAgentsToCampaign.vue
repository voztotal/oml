<template>
  <div class="card">
    <h1>{{ $t("campaign_info", { name: campaign["nombre"] }) }}</h1>
    <div class="p-fluid p-formgrid p-grid">
      <div class="p-field p-sm-12 p-md-6 p-lg-6 p-xl-6">
        <h2>{{ $tc("agent", 2) }}</h2>
        <AddAgents />
      </div>
      <div class="p-sm-12 p-md-6 p-lg-6 p-xl-6">
        <h2>{{ $tc("group", 2) }}</h2>
        <AddGroupAgents />
      </div>
    </div>
    <hr />
    <div class="p-grid p-mt-5">
      <div class="p-sm-12 p-md-12 p-lg-12 p-xl-12">
        <div class="p-d-flex p-jc-between p-ai-center">
          <div>
            <h2>{{ $t("agents_campaign") }}</h2>
          </div>
          <div class="p-grid">
            <Button
              class="p-mr-2 p-button-info"
              :label="$t('penalty')"
              icon="pi pi-info-circle"
              v-tooltip.left="
                $t('pages.add_agents_to_campaign.how_to_edit_penalty')
              "
            />
            <Button
              type="button"
              :label="$t('actions.save')"
              class="p-mr-2 p-button"
              icon="pi pi-save"
              @click="updateAgents()"
            />
          </div>
        </div>
        <AgentsCampaignTable />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import AddAgents from "@/components/campaigns/agents/AddAgents.vue";
import AddGroupAgents from "@/components/campaigns/agents/AddGroupAgents.vue";
import AgentsCampaignTable from "@/components/campaigns/agents/AgentsCampaignTable.vue";
import AgentsCampaignService from "@/services/agentsCampaignService.js";
import { getToasConfig } from "@/helpers/sweet_alerts_helper.js";

export default {
  components: {
    AgentsCampaignTable,
    AddGroupAgents,
    AddAgents,
  },
  data() {
    return {
      campaign_id: null,
    };
  },
  async created() {
    let element = window.parent.document.getElementById("add_agents_to_campaign")
    this.campaign_id = element.value
    this.agentsCampaignService = await new AgentsCampaignService();
    await this.initAgentsCampaign(this.campaign_id);
    await this.initActiveAgents()
  },
  methods: {
    ...mapActions(["initAgentsCampaign", "initActiveAgents", "initGroups"]),
    async updateAgents() {
      const agents = await this.agents_by_campaign.map((agent) => {
        return {
          agent_id: agent["agent_id"],
          agent_penalty: agent["agent_penalty"],
        };
      });
      if (this.agents_by_campaign.length == 0) {
        this.$swal({
          title: this.$t("sweet_alert.title.sure"),
          text: this.$t("pages.add_agents_to_campaign.empty_campaign_notice"),
          icon: this.$t("sweet_alert.icons.warning"),
          showCancelButton: true,
          confirmButtonText: this.$t("actions.yes"),
          cancelButtonText: this.$t("actions.no"),
          backdrop: false,
          reverseButtons: true,
        }).then(async (result) => {
          if (result.isConfirmed) {
            const { status, ok } =
              await this.agentsCampaignService.updateAgentsByCampaign({
                campaign_id: this.campaign_id,
                agents,
              });
            if (status == 200 && ok == true) {
              await this.initAgentsCampaign(this.campaign_id);
              await this.initActiveAgents()
              this.$swal(
                getToasConfig(
                  this.$t("sweet_alert.title.success"),
                  this.$t("pages.add_agents_to_campaign.agents_added_success"),
                  this.$t("sweet_alert.icons.success")
                )
              );
            } else {
              this.$swal(
                getToasConfig(
                  this.$t("sweet_alert.title.error"),
                  this.$t("pages.add_agents_to_campaign.agents_added_error"),
                  this.$t("sweet_alert.icons.error")
                )
              );
            }
          } else if (result.dismiss === this.$swal.DismissReason.cancel) {
            this.$swal(
              getToasConfig(
                this.$t("actions.cancelled"),
                this.$t("pages.add_agents_to_campaign.agents_not_save"),
                this.$t("sweet_alert.icons.error")
              )
            );
          }
        });
      } else {
        const { status, ok } =
          await this.agentsCampaignService.updateAgentsByCampaign({
            campaign_id: this.campaign_id,
            agents,
          });
        if (status == 200 && ok == true) {
          await this.initAgentsCampaign(this.campaign_id);
          await this.initActiveAgents()
          this.$swal(
            getToasConfig(
              this.$t("sweet_alert.title.success"),
              this.$t("pages.add_agents_to_campaign.agents_added_success"),
              this.$t("sweet_alert.icons.success")
            )
          );
        } else {
          this.$swal(
            getToasConfig(
              this.$t("sweet_alert.title.error"),
              this.$t("pages.add_agents_to_campaign.agents_added_error"),
              this.$t("sweet_alert.icons.error")
            )
          );
        }
      }
    },
  },
  computed: {
    ...mapState(["campaign", "agents_by_campaign"]),
  },
};
</script>
