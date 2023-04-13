<template>
  <div class="card">
    <div class="grid formgrid mt-2">
      <div class="field sm:col-12 md:col-12 lg:col-12 xl:col-12">
        <label id="message_transfer_from"
          >{{ $t("models.whatsapp.message_transfer.from") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-user"></i>
          </span>
          <InputText
            v-model="v$.form.from.$model"
            disabled
            placeholder="Disabled"
          />
        </div>
      </div>
    </div>
    <div class="grid formgrid mt-2">
      <div class="field sm:col-12 md:col-12 lg:col-12 xl:col-12">
        <label
          id="message_transfer_to"
          :class="{
            'p-error': v$.form.to.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.message_transfer.to") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-users"></i>
          </span>
          <Dropdown
            id="message_transfer_to"
            v-model="v$.form.to.$model"
            class="w-full"
            :class="{
              'p-invalid': v$.form.to.$invalid && submitted,
            }"
            :options="agents"
            placeholder="-----"
            optionLabel="name"
            optionValue="value"
            :emptyFilterMessage="$t('globals.without_data')"
            :filter="true"
            v-bind:filterPlaceholder="
              $t('globals.find_by', { field: $tc('globals.name') }, 1)
            "
          />
        </div>
        <small
          v-if="
            (v$.form.to.$invalid && submitted) || v$.form.to.$pending.$response
          "
          class="p-error"
        >
          {{
            v$.form.to.required.$message.replace(
              "Value",
              $t("models.whatsapp.message_transfer.to")
            )
          }}
        </small>
      </div>
    </div>
    <div class="flex justify-content-end flex-wrap mt-2">
      <div class="flex align-items-center">
        <Button
          class="p-button-danger p-button-outlined mr-2"
          :label="$t('globals.cancel')"
          @click="closeModal"
        />
        <Button
          :label="$t('globals.transfer')"
          icon="pi pi-arrows-h"
          @click="transfer(!v$.$invalid)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { FilterMatchMode } from 'primevue/api';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { mapActions, mapState } from 'vuex';
import { HTTP_STATUS } from '@/globals';

export default {
    setup: () => ({ v$: useVuelidate() }),
    validations () {
        return {
            form: {
                from: { required },
                to: { required }
            }
        };
    },
    inject: ['$helpers'],
    props: {
        formToCreate: {
            type: Boolean,
            default: true
        }
    },
    data () {
        return {
            form: {
                id: null,
                from: null,
                to: null
            },
            agents: [],
            submitted: false,
            filters: null
        };
    },
    created () {
        this.initializeData();
    },
    computed: {
        ...mapState(['agtWhatsManagementForm'])
    },
    methods: {
        ...mapActions(['agtWhatsManagementCreate', 'agtWhatsManagementInitData']),
        closeModal () {
            this.initializeData();
            this.$emit('closeModalEvent');
        },
        initializeData (open = false) {
            this.initFormData(open);
            this.submitted = false;
        },
        initFormData (open = false) {
            this.form.id = open ? this.agtWhatsManagementForm?.id : null;
            this.form.from = open ? this.agtWhatsManagementForm?.from : null;
            this.form.to = open ? this.agtWhatsManagementForm?.to : null;
        },
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        async transfer (isFormValid) {
            this.submitted = true;
            if (!isFormValid) {
                return null;
            }
            const { status, message } = await this.agtWhatsManagementCreate(
                this.form
            );
            if (status === HTTP_STATUS.SUCCESS) {
                await this.agtWhatsManagementInitData();
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
            this.initializeData();
        }
    },
    watch: {
        agtWhatsManagementForm: {
            handler () {
                if (this.agtWhatsManagementForm) {
                    this.initFormData();
                }
            },
            deep: true,
            immediate: true
        }
    }
};
</script>
