<template>
  <div class="card">
    <DataTable
      :value="agtWhatsTemplates"
      class="p-datatable-sm"
      showGridlines
      :scrollable="true"
      scrollHeight="600px"
      responsiveLayout="scroll"
      dataKey="id"
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      :paginator="true"
      paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      :currentPageReportTemplate="
        $t('globals.showing_datatable_info', {
          first: '{first}',
          last: '{last}',
          totalRecords: '{totalRecords}',
        })
      "
      :filters="filters"
      :globalFilterFields="['nombre']"
    >
      <template #header>
        <div class="flex justify-content-between flex-wrap">
          <div class="flex align-items-center justify-content-center">
            <Button
              type="button"
              icon="pi pi-filter-slash"
              :label="$t('globals.clean_filter')"
              class="p-button-outlined"
              @click="clearFilter()"
            />
          </div>
          <div class="flex align-items-center justify-content-center">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText
                v-model="filters['global'].value"
                icon="pi pi-check"
                :placeholder="
                  $t('globals.find_by', { field: $tc('globals.name', 1) })
                "
              />
            </span>
          </div>
        </div>
      </template>
      <template #empty> {{ $t("globals.without_data") }} </template>
      <template #loading> {{ $t("globals.load_info") }} </template>
      <Column
        field="nombre"
        style="max-width: 15rem"
        :sortable="true"
        :header="$t('models.whatsapp.provider.nombre')"
      ></Column>
      <Column
        field="configuracion"
        :header="$t('models.whatsapp.provider.nombre')"
      ></Column>
      <!-- <Column
          field="tipo_proveedor"
          :header="$t('models.whatsapp.provider.tipo_proveedor')"
        >
          <template #body="slotProps">
            {{ slotProps.data.tipo_proveedor }}
          </template>
        </Column> -->
      <Column :header="$tc('globals.option', 2)" style="max-width: 10rem">
        <template #body="slotProps">
          <Button
            icon="pi pi-send"
            class="p-button-info ml-2"
            @click="send(slotProps.data)"
            v-tooltip.top="$t('globals.edit')"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { FilterMatchMode } from 'primevue/api';

export default {
    inject: ['$helpers'],
    data () {
        return {
            filters: null
        };
    },
    created () {
        this.initFilters();
        this.agtWhatsTemplatesInit();
    },
    computed: {
        ...mapState(['agtWhatsTemplates'])
    },
    methods: {
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        send (template) {
            this.agtWhatsTemplateSendMsg(template);
        },
        ...mapActions(['agtWhatsTemplatesInit', 'agtWhatsTemplateSendMsg'])
    },
    watch: {
        agtWhatsTemplates: {
            handler () {},
            deep: true,
            immediate: true
        }
    }
};
</script>
