<template>
  <div class="card">
    <div class="grid formgrid mt-4">
      <div class="field col-6">
        <label
          id="whatsapp_provider_nombre"
          :class="{
            'p-error': v$.supWhatsappProviderForm.nombre.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.provider.nombre") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-list"></i>
          </span>
          <InputText
            id="whatsapp_provider_nombre"
            :class="{
              'p-invalid':
                v$.supWhatsappProviderForm.nombre.$invalid && submitted,
            }"
            v-model="v$.supWhatsappProviderForm.nombre.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappProviderForm.nombre.$invalid && submitted) ||
            v$.supWhatsappProviderForm.nombre.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappProviderForm.nombre.required.$message.replace(
              "Value",
              $t("models.whatsapp.provider.nombre")
            )
          }}</small
        >
      </div>
      <div class="field col-6">
        <label
          id="whatsapp_provider_proveedor"
          :class="{
            'p-error':
              v$.supWhatsappProviderForm.tipo_proveedor.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.provider.tipo_proveedor") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-sitemap"></i>
          </span>
          <Dropdown
            id="whatsapp_provider_proveedor"
            v-model="v$.supWhatsappProviderForm.tipo_proveedor.$model"
            class="w-full"
            :class="{
              'p-invalid':
                v$.supWhatsappProviderForm.tipo_proveedor.$invalid && submitted,
            }"
            :options="providers"
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
            (v$.supWhatsappProviderForm.tipo_proveedor.$invalid && submitted) ||
            v$.supWhatsappProviderForm.tipo_proveedor.$pending.$response
          "
          class="p-error"
        >
          {{
            v$.supWhatsappProviderForm.tipo_proveedor.required.$message.replace(
              "Value",
              $t("models.whatsapp.provider.tipo_proveedor")
            )
          }}
        </small>
      </div>
    </div>
    <div class="grid formgrid mt-4">
      <div class="field col-6">
        <label
          id="whatsapp_provider_identificador"
          :class="{
            'p-error':
              v$.supWhatsappProviderForm.identificador.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.provider.identificador") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-id-card"></i>
          </span>
          <InputText
            id="whatsapp_provider_identificador"
            :class="{
              'p-invalid':
                v$.supWhatsappProviderForm.identificador.$invalid && submitted,
            }"
            v-model="v$.supWhatsappProviderForm.identificador.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappProviderForm.identificador.$invalid && submitted) ||
            v$.supWhatsappProviderForm.identificador.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappProviderForm.identificador.required.$message.replace(
              "Value",
              $t("models.whatsapp.provider.identificador")
            )
          }}</small
        >
      </div>
      <div class="field col-6">
        <label
          id="whatsapp_provider_token_autorizacion"
          :class="{
            'p-error':
              v$.supWhatsappProviderForm.token_autorizacion.$invalid &&
              submitted,
          }"
          >{{ $t("models.whatsapp.provider.token_autorizacion") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-key"></i>
          </span>
          <Password
            id="whatsapp_provider_token_autorizacion"
            toggleMask
            :feedback="false"
            :class="{
              'p-invalid':
                v$.supWhatsappProviderForm.token_autorizacion.$invalid &&
                submitted,
            }"
            v-model="v$.supWhatsappProviderForm.token_autorizacion.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappProviderForm.token_autorizacion.$invalid &&
              submitted) ||
            v$.supWhatsappProviderForm.token_autorizacion.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappProviderForm.token_autorizacion.required.$message.replace(
              "Value",
              $t("models.whatsapp.provider.token_autorizacion")
            )
          }}</small
        >
      </div>
    </div>
    <div class="flex justify-content-end flex-wrap">
      <div class="flex align-items-center">
        <Button
          :label="$t('globals.save')"
          icon="pi pi-save"
          class="mt-4"
          @click="saveExternalSite(!v$.$invalid)"
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
import { PROVIDER_TYPES } from '@/globals/supervisor/whatsapp/provider';

export default {
    setup: () => ({ v$: useVuelidate() }),
    validations () {
        return {
            supWhatsappProviderForm: {
                nombre: { required },
                tipo_proveedor: { required },
                identificador: { required },
                token_autorizacion: { required }
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
            supWhatsappProviderForm: {
                id: null,
                nombre: '',
                tipo_proveedor: 0,
                identificador: '',
                token_autorizacion: ''
            },
            submitted: false,
            filters: null,
            providers: [
                { name: '-------', value: null },
                {
                    name: this.$t('forms.whatsapp.provider.types.twilio'),
                    value: PROVIDER_TYPES.TWILIO
                },
                {
                    name: this.$t('forms.whatsapp.provider.types.meta'),
                    value: PROVIDER_TYPES.META
                },
                {
                    name: this.$t('forms.whatsapp.provider.types.gupshup'),
                    value: PROVIDER_TYPES.GUPSHUP
                }
            ]
        };
    },
    created () {
        this.initializeData();
    },
    computed: {
        ...mapState(['supWhatsappProvider'])
    },
    methods: {
        ...mapActions([
            'createWhatsappProvider',
            'updateWhatsappProvider',
            'initExternalSiteAuthentications'
        ]),
        initializeData () {
            this.initFormData();
            this.submitted = false;
        },
        initFormData () {
            this.supWhatsappProviderForm.id = this.supWhatsappProvider.id;
            this.supWhatsappProviderForm.nombre = this.supWhatsappProvider.nombre;
            this.supWhatsappProviderForm.tipo_proveedor =
        this.supWhatsappProvider.tipo_proveedor;
            this.supWhatsappProviderForm.identificador =
        this.supWhatsappProvider.identificador;
            this.supWhatsappProviderForm.token_autorizacion =
        this.supWhatsappProvider.token_autorizacion;
        },
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        async saveExternalSite (isFormValid) {
            this.submitted = true;
            if (!isFormValid) {
                return null;
            }
            var response = null;
            if (this.formToCreate) {
                response = await this.createWhatsappProvider(
                    this.supWhatsappProviderForm
                );
            } else {
                response = await this.updateWhatsappProvider({
                    id: this.supWhatsappProvider.id,
                    data: this.supWhatsappProviderForm
                });
            }
            const { status, message } = response;
            if (status === 'SUCCESS') {
                this.$router.push({ name: 'supervisor_whatsapp_providers' });
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
        }
    },
    watch: {
        supWhatsappProvider: {
            handler () {
                if (this.supWhatsappProvider) {
                    this.initFormData();
                }
            },
            deep: true,
            immediate: true
        }
    }
};
</script>
