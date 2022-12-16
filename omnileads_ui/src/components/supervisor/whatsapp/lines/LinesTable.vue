<template>
  <div class="card">
    <DataTable
      :value="supWhatsappLines"
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
            <Button
              class="ml-2 p-button-info"
              icon="pi pi-plus"
              v-tooltip.top="$t('globals.new')"
              @click="newLine"
            />
          </div>
        </div>
      </template>
      <template #empty> {{ $t("globals.without_data") }} </template>
      <template #loading> {{ $t("globals.load_info") }} </template>
      <Column
        field="nombre"
        :header="$t('models.whatsapp.line.nombre')"
      ></Column>
      <Column
        field="numero"
        :header="$t('models.whatsapp.line.numero')"
      ></Column>
      <!-- <Column
        field="es_verificado"
        :header="$t('models.whatsapp.line.es_verificado')"
      ></Column> -->
      <Column
        field="proveedor"
        :header="$t('models.whatsapp.line.proveedor')"
      >
        <template #body="slotProps">
          {{ getProvider(slotProps.data.proveedor) }}
        </template>
      </Column>
      <Column
        field="identificador"
        :header="$t('models.whatsapp.line.identificador')"
      ></Column>
      <Column
        field="token_validacion"
        :header="$t('models.whatsapp.line.token_validacion')"
      ></Column>
      <Column :header="$tc('globals.option', 2)" :exportable="false">
        <template #body="slotProps">
          <Button
            icon="pi pi-pencil"
            class="p-button-warning ml-2"
            @click="edit(slotProps.data)"
            v-tooltip.top="$t('globals.edit')"
          />
          <Button
            icon="pi pi-trash"
            class="p-button-danger ml-2"
            @click="remove(slotProps.data.id)"
            v-tooltip.top="$t('globals.delete')"
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
    },
    computed: {
        ...mapState(['supWhatsappLines', 'supWhatsappProviders'])
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
        edit (line) {
            this.initWhatsappLine({ line });
            this.$emit('handleModalEvent', {
                showModal: true, line
            });
        },
        newLine () {
            this.$emit('handleModalEvent', {
                showModal: true, formToCreate: true
            });
        },
        getProvider (id) {
            if (this.supWhatsappProviders.length > 0) {
                return this.supWhatsappProviders.find(p => p.id === parseInt(id)).nombre;
            }
            return '---------';
        },
        async remove (id) {
            this.$swal({
                title: this.$t('globals.sure_notification'),
                icon: this.$t('globals.icon_warning'),
                showCancelButton: true,
                confirmButtonText: this.$t('globals.yes'),
                cancelButtonText: this.$t('globals.no'),
                confirmButtonColor: '#4CAF50',
                cancelButtonColor: '#D32F2F',
                backdrop: false,
                reverseButtons: true
            }).then(async (result) => {
                if (result.isConfirmed) {
                    this.$swal.fire({
                        title: this.$t('globals.processing_request'),
                        timerProgressBar: true,
                        allowOutsideClick: false,
                        didOpen: () => {
                            this.$swal.showLoading();
                        }
                    });
                    const { status, message } = await this.deleteWhatsappLine(id);
                    this.$swal.close();
                    if (status === 'SUCCESS') {
                        this.initWhatsappLines();
                        this.$swal(
                            this.$helpers.getToasConfig(
                                this.$t('globals.success_notification'),
                                message,
                                this.$t('globals.icon_success')
                            )
                        );
                    } else {
                        this.$swal(
                            this.$helpers.getToasConfig(
                                this.$t('globals.error_notification'),
                                message,
                                this.$t('globals.icon_error')
                            )
                        );
                    }
                } else if (result.dismiss === this.$swal.DismissReason.cancel) {
                    this.$swal(
                        this.$helpers.getToasConfig(
                            this.$t('globals.cancelled'),
                            this.$tc('globals.error_to_deleted_type', {
                                type: this.$tc('globals.whatsapp.line')
                            }),
                            this.$t('globals.icon_error')
                        )
                    );
                }
            });
        },
        ...mapActions(['deleteWhatsappLine', 'initWhatsappLines', 'initWhatsappLine'])
    },
    watch: {
        supWhatsappLines: {
            handler () {},
            deep: true,
            immediate: true
        },
        supWhatsappProviders: {
            handler () {},
            deep: true,
            immediate: true
        }
    }
};
</script>
