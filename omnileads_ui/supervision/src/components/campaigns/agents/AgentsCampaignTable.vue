<template>
  <div class="card">
    <DataTable
      :value="agents_by_campaign"
      class="p-datatable-sm editable-cells-table"
      showGridlines
      :scrollable="true"
      scrollHeight="600px"
      responsiveLayout="scroll"
      dataKey="id"
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      :paginator="true"
      paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      currentPageReportTemplate="Mostrando del {first} al {last} de {totalRecords}"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="[
        'agent_full_name',
        'agent_penalty',
        'representative.name',
      ]"
      editMode="cell"
      @cell-edit-complete="onCellEditComplete"
    >
      <template #header>
        <div class="p-d-flex p-jc-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            :label="$t('clean_object', { object: 'filtros' })"
            class="p-button-outlined"
            @click="clearFilter()"
          />
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              icon="pi pi-check"
              :placeholder="$t('find_by', { field: $t('name') })"
            />
          </span>
        </div>
      </template>
      <template #empty>
        {{ $t("pages.add_agents_to_campaign.empty_agents") }}</template
      >
      <template #loading>
        {{ $t("pages.add_agents_to_campaign.load_info") }}
      </template>
      <Column
        field="agent_full_name"
        :header="$t('agent_campaign.name')"
      ></Column>
      <Column
        field="agent_username"
        :header="$t('agent_campaign.username')"
      ></Column>
      <Column
        field="agent_sip_id"
        :header="$t('agent_campaign.sip')"
        :sortable="true"
      ></Column>
      <Column
        field="agent_penalty"
        :header="$t('agent_campaign.penalty')"
        :sortable="true"
      >
        <template #editor="{ data, field }">
          <Dropdown
            v-model="data[field]"
            :options="penalties"
            optionLabel="label"
            optionValue="value"
            :placeholder="
              $t('pages.add_agents_to_campaign.select_type', {
                type: 'penalty',
              })
            "
          >
            <template #option="slotProps">
              <span>{{ slotProps.option.label }}</span>
            </template>
          </Dropdown>
        </template>
      </Column>
      <Column :header="$tc('option')" :exportable="false">
        <template #body="slotProps">
          <Button
            icon="pi pi-trash"
            class="p-button-danger"
            @click="removeAgent(slotProps.data.agent_id)"
            v-tooltip.top="$t('pages.add_agents_to_campaign.delete_agent')"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { FilterMatchMode } from "primevue/api";
import { getToasConfig } from "@/helpers/sweet_alerts_helper.js";

export default {
  data() {
    return {
      filters: null,
      penalties: [
        { label: `${this.$t('penalty')} 0`, value: 0 },
        { label: `${this.$t('penalty')} 1`, value: 1 },
        { label: `${this.$t('penalty')} 2`, value: 2 },
        { label: `${this.$t('penalty')} 3`, value: 3 },
        { label: `${this.$t('penalty')} 4`, value: 4 },
        { label: `${this.$t('penalty')} 5`, value: 5 },
        { label: `${this.$t('penalty')} 6`, value: 6 },
        { label: `${this.$t('penalty')} 7`, value: 7 },
        { label: `${this.$t('penalty')} 8`, value: 8 },
        { label: `${this.$t('penalty')} 9`, value: 9 },
      ],
    };
  },
  created() {
    this.initFilters();
  },
  methods: {
    clearFilter() {
      this.initFilters();
    },
    initFilters() {
      this.filters = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      };
    },
    removeAgent(agent_id) {
      this.removeAgentOfCampaign(agent_id);
      this.$swal(
        getToasConfig(
          this.$t("sweet_alert.title.success"),
          this.$t("pages.add_agents_to_campaign.agent_deleted_success"),
          this.$t("sweet_alert.icons.success")
        )
      );
    },
    onCellEditComplete(event) {
      let { data, newValue } = event;
      this.updateAgentPenalty({
        agent_id: data["agent_id"],
        penalty: newValue,
      });
      this.$swal(
        getToasConfig(
          this.$t("sweet_alert.title.success"),
          this.$t("pages.add_agents_to_campaign.penalty_updated_success"),
          this.$t("sweet_alert.icons.success")
        )
      );
    },
    ...mapActions(["removeAgentOfCampaign", "updateAgentPenalty"]),
  },
  watch: {
    agents_by_campaign: {
      deep: true,
      handler() {},
    },
  },
  computed: {
    ...mapGetters({
      agents_by_campaign: "getAgentsByCampaign",
    }),
  },
};
</script>
