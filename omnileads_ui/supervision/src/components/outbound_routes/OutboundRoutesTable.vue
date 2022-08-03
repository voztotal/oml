<template>
  <div class="card">
    <DataTable
      :value="outboundRoutes"
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
      filterDisplay="menu"
      :globalFilterFields="['nombre']"
      :reorderableColumns="true" @rowReorder="onRowReorder"
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
      <Column :rowReorder="true" headerStyle="width: 1rem" :reorderableColumn="false" />
      <Column
        field="nombre"
        :sortable="true"
        :header="$t('models.outbound_route.name')"
      ></Column>
      <Column
        field="ring_time"
        :sortable="true"
        :header="$t('models.outbound_route.ring_time')"
      ></Column>
      <Column
        field="dial_options"
        :header="$t('models.outbound_route.dial_options')"
      ></Column>
      <Column
        :header="$tc('globals.option', 2)"
        style="max-width: 25rem"
        :exportable="false"
      >
        <template #body="slotProps">
          <Button
            icon="pi pi-eye"
            class="p-button-info ml-2"
            @click="detail(slotProps.data)"
            v-tooltip.top="$t('globals.show')"
          />
          <Button
            icon="pi pi-pencil"
            class="p-button-warning ml-2"
            @click="edit(slotProps.data.id)"
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
    <ModalOutboundRouteDetail :outboundRoute='outboundRouteDetail' :showModal='showModalDetail' @handleModalDetailEvent='handleModalDetail' />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { FilterMatchMode } from 'primevue/api';
import ModalOutboundRouteDetail from '@/components/outbound_routes/ModalOutboundRouteDetail';

export default {
    inject: ['$helpers'],
    props: {
        outboundRoutes: {
            type: Array,
            default: () => []
        }
    },
    components: {
        ModalOutboundRouteDetail
    },
    data () {
        return {
            filters: null,
            showModalDetail: false,
            outboundRouteDetail: {}
        };
    },
    created () {
        this.initFilters();
    },
    computed: {
        ...mapState(['orphanTrunks'])
    },
    methods: {
        ...mapActions(['initOutboundRoutes', 'deleteOutboundRoute', 'initOutboundRouteOrphanTrunks']),
        onRowReorder (event) {
            console.log('onRowReorder');
            console.log(event);
            // this.outboundRoutes = event.value;
            // this.$toast.add({severity:'success', summary: 'Rows Reordered', life: 3000});
        },
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        edit (id) {
            this.$router.push({
                name: 'outbound_routes_edit',
                params: { id }
            });
        },
        detail (outboundRoute) {
            this.showModalDetail = true;
            this.outboundRouteDetail = outboundRoute;
        },
        handleModalDetail (showModal) {
            this.showModalDetail = showModal;
        },
        getOrphanTrunksMessage () {
            if (this.orphanTrunks.length > 0) {
                var message = '<p>Al eliminar la ruta saliente los siguientes Troncales Sip quedarán sin ser usados por rutas Salientes</p>';
                message += '<ul>';
                this.orphanTrunsks.forEach(trunk => {
                    message += `<li>${trunk.nombre}</li>`;
                });
                message += '</ul>';
                return message;
            } else {
                return null;
            }
        },
        async remove (id) {
            await this.initOutboundRouteOrphanTrunks(id);
            this.$swal({
                title: this.$t('globals.sure_notification'),
                icon: this.$t('globals.icon_warning'),
                showCancelButton: true,
                html: this.getOrphanTrunksMessage(),
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
                    const response = await this.deleteOutboundRoute(id);
                    this.$swal.close();
                    const { status, message } = response;
                    if (status === 'SUCCESS') {
                        this.initOutboundRoutes();
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
                                type: this.$tc('globals.outbound_route')
                            }),
                            this.$t('globals.icon_error')
                        )
                    );
                }
            });
        }
    },
    watch: {
        outboundRoutes: {
            handler () {},
            deep: true,
            immediate: true
        }
    }
};
</script>
