<template>
  <!-- eslint-disable vue/no-v-model-argument -->
  <DataTable
    :value="tableData"
    ref="dt"
    :paginator="true"
    class="p-datatable-customers"
    showGridlines
    :scrollable="true"
    scrollHeight="600px"
    :rows="10"
    :rowsPerPageOptions="[10, 20, 50]"
    paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    :currentPageReportTemplate="
      $t('globals.showing_datatable_info', {
        first: '{first}',
        last: '{last}',
        totalRecords: '{totalRecords}',
      })
    "
    :filters="filters"
    filterDisplay="menu"
    :loading="loading"
    stripedRows
    responsiveLayout="scroll"
    :globalFilterFields="['username', 'object', 'name', 'action', 'date']"
  >
    <template #header>
      <div class="flex justify-content-between flex-wrap">
        <div class="flex align-items-center justify-content-center">
          <Button
            icon="pi pi-external-link"
            class="p-button-info"
            :label="$t('globals.export_type', { type: 'CSV' })"
            @click="exportCSV($event)"
          />
        </div>
        <div class="flex align-items-center justify-content-center">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            :label="$t('globals.clean_filter')"
            class="p-button-outlined mr-2"
            @click="clearFilter()"
          />
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              icon="pi pi-check"
              :placeholder="$tc('globals.find', 2)"
            />
          </span>
        </div>
      </div>
    </template>
    <template #empty> {{ $t("globals.without_data") }} </template>
    <template #loading> {{ $t("globals.load_info") }} </template>
    <Column
      field="username"
      :header="$tc('models.audit.user')"
      :sortable="true"
    ></Column>
    <Column
      field="object"
      :header="$tc('models.audit.object')"
      :sortable="true"
    ></Column>
    <Column
      field="name"
      :header="$tc('models.audit.name')"
      :sortable="true"
    ></Column>
    <Column
      field="action"
      :header="$tc('models.audit.action')"
      :sortable="true"
    ></Column>
    <Column
      field="additional_information"
      :header="$tc('models.audit.additional_information')"
    ></Column>
    <Column
      field="date"
      :header="$tc('models.audit.datetime')"
      :sortable="true"
    ></Column>
  </DataTable>
</template>
<script>
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import { ref } from 'vue';

export default {
    props: {
        tableData: Object,
        loading: Boolean
    },
    setup () {
        const filters = ref({
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            username: {
                operator: FilterOperator.AND,
                constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
            },
            action: {
                operator: FilterOperator.AND,
                constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
            },
            date: {
                operator: FilterOperator.AND,
                constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
            }
        });

        const dates = ref();
        const dt = ref();

        const clearFilter = () => {
            initFilters();
        };
        const initFilters = () => {
            filters.value = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                username: {
                    operator: FilterOperator.AND,
                    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
                },
                action: {
                    operator: FilterOperator.AND,
                    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
                },
                date: {
                    operator: FilterOperator.AND,
                    constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
                }
            };
        };
        const exportCSV = () => {
            dt.value.exportCSV();
        };

        return { dates, filters, clearFilter, initFilters, dt, exportCSV };
    }
};
</script>
