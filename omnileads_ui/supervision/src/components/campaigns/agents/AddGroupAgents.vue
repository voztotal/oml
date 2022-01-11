<template>
  <div>
    <div class="p-field p-col-12 p-md-12 p-lg-12">
      <Dropdown
        v-model="selectedGroup"
        :options="groupsSelectize"
        optionLabel="group"
        :placeholder="$tc('select_a', 1, { field: $tc('group', 1) })"
        :filter="true"
        v-bind:filterPlaceholder="$t('find_by', { field: $t('name') })"
      />
    </div>
    <div class="p-field p-col-12 p-md-4 p-lg-4">
      <Button
        type="button"
        class="p-button p-button-secondary"
        v-bind:label="$t('actions.add')"
        @click="addGroup"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { getToasConfig } from "@/helpers/sweet_alerts_helper.js";

export default {
  data() {
    return {
      groupsSelectize: [],
      selectedGroup: null,
    };
  },
  methods: {
    addGroup() {
      if (this.selectedGroup) {
        var group_id = this.selectedGroup["value"];
        var group = this.groups.find(
          (group) => group_id == group["group"]["id"]
        );
        var existing_agents = [];
        group["agents"].forEach((agent) => {
          if (
            this.agents_by_campaign.find(
              (a) => a["agent_id"] == agent["agent_id"]
            )
          ) {
            existing_agents.push(agent["agent_username"]);
          } else {
            this.addAgentToCampaign(agent);
          }
        });
        this.selectedGroup = null;
        if (existing_agents.length > 0) {
          this.$swal(
            getToasConfig(
              this.$t("sweet_alert.title.warning"),
              this.$t(
                "pages.add_agents_to_campaign.already_agents_in_campaign",
                { agents: existing_agents.join(" - ") }
              ),
              this.$t("sweet_alert.icons.warning")
            )
          );
        } else {
          this.$swal(
            getToasConfig(
              this.$t("sweet_alert.title.success"),
              this.$t("pages.add_agents_to_campaign.group_added_success"),
              this.$t("sweet_alert.icons.success")
            )
          );
        }
      } else {
        this.$swal(
          getToasConfig(
            this.$t("sweet_alert.title.warning"),
            this.$t("pages.add_agents_to_campaign.not_select_type", {
              type: this.$t("group"),
            }),
            this.$t("sweet_alert.icons.warning")
          )
        );
      }
    },
    updatedGroupsSelectize() {
      this.groupsSelectize = this.groups.map((group) => {
        return {
          group: group["group"]["name"],
          value: group["group"]["id"],
        };
      });
    },
    ...mapActions(["addAgentToCampaign"]),
  },
  watch: {
    agents_by_campaign: {
      deep: true,
      handler() {},
    },
    groups: {
      deep: true,
      handler() {
        this.updatedGroupsSelectize();
      },
    },
  },
  computed: {
    ...mapGetters({
      agents_by_campaign: "getAgentsByCampaign",
      groups: "getGroups",
    }),
  },
};
</script>

