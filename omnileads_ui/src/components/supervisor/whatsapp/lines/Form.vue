<template>
  <div class="card">
    <div class="grid formgrid">
      <div class="field col-6">
        <label
          id="whatsapp_line_nombre"
          :class="{
            'p-error': v$.supWhatsappLineForm.nombre.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.line.nombre") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-list"></i>
          </span>
          <InputText
            id="whatsapp_line_nombre"
            :class="{
              'p-invalid':
                v$.supWhatsappLineForm.nombre.$invalid && submitted,
            }"
            v-model="v$.supWhatsappLineForm.nombre.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappLineForm.nombre.$invalid && submitted) ||
            v$.supWhatsappLineForm.nombre.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappLineForm.nombre.required.$message.replace(
              "Value",
              $t("models.whatsapp.line.nombre")
            )
          }}</small
        >
      </div>
      <div class="field col-6">
        <label
          id="whatsapp_line_numero"
          :class="{
            'p-error': v$.supWhatsappLineForm.numero.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.line.numero") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-phone"></i>
          </span>
          <InputMask
            id="whatsapp_line_numero"
            mask="999-999-9999"
            placeholder="999-999-9999"
            :class="{
              'p-invalid':
                v$.supWhatsappLineForm.numero.$invalid && submitted,
            }"
            v-model="v$.supWhatsappLineForm.numero.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappLineForm.numero.$invalid && submitted) ||
            v$.supWhatsappLineForm.numero.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappLineForm.numero.required.$message.replace(
              "Value",
              $t("models.whatsapp.line.numero")
            )
          }}</small
        >
      </div>
    </div>
    <div class="grid formgrid mt-4">
      <div class="field col-6">
        <label
          id="whatsapp_line_identificador"
          :class="{
            'p-error':
              v$.supWhatsappLineForm.identificador.$invalid && submitted,
          }"
          >{{ $t("models.whatsapp.line.identificador") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-id-card"></i>
          </span>
          <InputText
            id="whatsapp_line_identificador"
            :class="{
              'p-invalid':
                v$.supWhatsappLineForm.identificador.$invalid && submitted,
            }"
            v-model="v$.supWhatsappLineForm.identificador.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappLineForm.identificador.$invalid && submitted) ||
            v$.supWhatsappLineForm.identificador.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappLineForm.identificador.required.$message.replace(
              "Value",
              $t("models.whatsapp.line.identificador")
            )
          }}</small
        >
      </div>
      <div class="field col-6">
        <label
          id="whatsapp_line_token_validacion"
          :class="{
            'p-error':
              v$.supWhatsappLineForm.token_validacion.$invalid &&
              submitted,
          }"
          >{{ $t("models.whatsapp.line.token_validacion") }}*</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-key"></i>
          </span>
          <Password
            id="whatsapp_line_token_validacion"
            toggleMask
            :feedback="false"
            :class="{
              'p-invalid':
                v$.supWhatsappLineForm.token_validacion.$invalid &&
                submitted,
            }"
            v-model="v$.supWhatsappLineForm.token_validacion.$model"
          />
        </div>
        <small
          v-if="
            (v$.supWhatsappLineForm.token_validacion.$invalid &&
              submitted) ||
            v$.supWhatsappLineForm.token_validacion.$pending.$response
          "
          class="p-error"
          >{{
            v$.supWhatsappLineForm.token_validacion.required.$message.replace(
              "Value",
              $t("models.whatsapp.line.token_validacion")
            )
          }}</small
        >
      </div>
    </div>
    <div class="grid formgrid mt-4">
        <div class="field col-6">
            <label
              id="whatsapp_line_tipo_de_destino"
              :class="{
                'p-error': v$.supWhatsappLineForm.tipo_de_destino.$invalid && submitted,
              }"
              >{{ $t("models.whatsapp.line.tipo_de_destino") }}*</label
            >
            <Dropdown
              v-model="v$.supWhatsappLineForm.tipo_de_destino.$model"
              class="w-full mt-2"
              :class="{
                'p-invalid': v$.supWhatsappLineForm.tipo_de_destino.$invalid && submitted,
              }"
              :options="destinationTypes"
              placeholder="-----"
              optionLabel="option"
              optionValue="value"
              @change="getDestinations"
              :emptyFilterMessage="$t('globals.without_data')"
            />
            <small
              v-if="
                (v$.supWhatsappLineForm.tipo_de_destino.$invalid && submitted) ||
                v$.supWhatsappLineForm.tipo_de_destino.$pending.$response
              "
              class="p-error"
              >{{
                v$.supWhatsappLineForm.tipo_de_destino.required.$message.replace(
                  "Value",
                  $t("models.whatsapp.line.tipo_de_destino")
                )
              }}</small
            >
        </div>
        <div class="field col-6">
            <label
              id="pause_type"
              :class="{
                'p-error': v$.supWhatsappLineForm.destino.$invalid && submitted,
              }"
              >{{ $t("models.whatsapp.line.destino") }}*</label
            >
            <Dropdown
              v-model="v$.supWhatsappLineForm.destino.$model"
              class="w-full mt-2"
              :class="{
                'p-invalid': v$.supWhatsappLineForm.destino.$invalid && submitted,
              }"
              :options="destinationsByType"
              placeholder="-----"
              optionLabel="nombre"
              optionValue="id"
              :emptyFilterMessage="$t('globals.without_data')"
            />
            <small
              v-if="
                (v$.supWhatsappLineForm.destino.$invalid && submitted) ||
                v$.supWhatsappLineForm.destino.$pending.$response
              "
              class="p-error"
              >{{
                v$.supWhatsappLineForm.destino.required.$message.replace(
                  "Value",
                  $t("models.whatsapp.line.destino")
                )
              }}</small
            >
        </div>
    </div>
    <div class="grid formgrid mt-4">
        <div class="field col-6">
            <label
              id="whatsapp_line_proveedor"
              :class="{
                'p-error': v$.supWhatsappLineForm.proveedor.$invalid && submitted,
              }"
              >{{ $t("models.whatsapp.line.proveedor") }}*</label
            >
            <Dropdown
              v-model="v$.supWhatsappLineForm.proveedor.$model"
              class="w-full mt-2"
              :class="{
                'p-invalid': v$.supWhatsappLineForm.proveedor.$invalid && submitted,
              }"
              :options="supWhatsappProviders"
              placeholder="-----"
              optionLabel="nombre"
              optionValue="id"
              :emptyFilterMessage="$t('globals.without_data')"
            />
            <small
              v-if="
                (v$.supWhatsappLineForm.proveedor.$invalid && submitted) ||
                v$.supWhatsappLineForm.proveedor.$pending.$response
              "
              class="p-error"
              >{{
                v$.supWhatsappLineForm.proveedor.required.$message.replace(
                  "Value",
                  $t("models.whatsapp.line.proveedor")
                )
              }}</small
            >
        </div>
    </div>
    <div class="grid formgrid mt-4">
      <div class="field col-6">
        <label
          id="whatsapp_line_mensaje_bienvenida"
          >{{ $t("models.whatsapp.line.mensaje_bienvenida") }}</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-comment"></i>
          </span>
          <Textarea
            id="whatsapp_line_mensaje_bienvenida"
            v-model="supWhatsappLineForm.mensaje_bienvenida"
            rows="5" cols="30"
          />
        </div>
      </div>
      <div class="field col-6">
        <label
          id="whatsapp_line_mensaje_despedida"
          >{{ $t("models.whatsapp.line.mensaje_despedida") }}</label
        >
        <div class="p-inputgroup mt-2">
          <span class="p-inputgroup-addon">
            <i class="pi pi-comment"></i>
          </span>
          <Textarea
            id="whatsapp_line_mensaje_despedida"
            v-model="supWhatsappLineForm.mensaje_despedida"
            rows="5" cols="30"
          />
        </div>
      </div>
    </div>
    <div class="flex justify-content-end flex-wrap mt-4">
      <div class="flex align-items-center">
        <Button
          class="p-button-danger p-button-outlined mr-2"
          :label="$t('globals.cancel')"
          @click="closeModal"
        />
        <Button
          :label="$t('globals.save')"
          icon="pi pi-save"
          @click="save(!v$.$invalid)"
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

export default {
    setup: () => ({ v$: useVuelidate() }),
    validations () {
        return {
            supWhatsappLineForm: {
                nombre: { required },
                proveedor: { required },
                numero: { required },
                identificador: { required },
                token_validacion: { required },
                destino: { required },
                tipo_de_destino: { required }
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
            supWhatsappLineForm: {
                id: null,
                nombre: '',
                proveedor: null,
                numero: '',
                identificador: '',
                es_verificado: false,
                token_validacion: '',
                destino: null,
                tipo_de_destino: null,
                mensaje_bienvenida: '',
                mensaje_despedida: ''
            },
            submitted: false,
            filters: null,
            destinationTypes: [
                { option: this.$t('forms.inbound_route.destination_types.campaign'), value: 1 },
                { option: this.$t('forms.inbound_route.destination_types.validation_date'), value: 2 },
                { option: this.$t('forms.inbound_route.destination_types.ivr'), value: 3 },
                { option: this.$t('forms.inbound_route.destination_types.hangup'), value: 5 },
                { option: this.$t('forms.inbound_route.destination_types.id_client'), value: 9 },
                { option: this.$t('forms.inbound_route.destination_types.custom_dst'), value: 7 }
            ],
            destinationsByType: []
        };
    },
    async created () {
        await this.initInboundRoutesDestinations();
        await this.initWhatsappProviders();
        this.initializeData();
    },
    computed: {
        ...mapState(['supWhatsappLine', 'supWhatsappProviders', 'destinations'])
    },
    methods: {
        ...mapActions([
            'createWhatsappLine',
            'updateWhatsappLine',
            'initWhatsappProviders',
            'initWhatsappLines',
            'initInboundRoutesDestinations'
        ]),
        closeModal () {
            this.$emit('closeModalEvent');
        },
        initializeData () {
            this.initFormData();
            this.submitted = false;
        },
        initFormData () {
            this.supWhatsappLineForm.id = this.supWhatsappLine.id;
            this.supWhatsappLineForm.nombre = this.supWhatsappLine.nombre;
            this.supWhatsappLineForm.proveedor = this.supWhatsappLine.proveedor;
            this.supWhatsappLineForm.numero = this.supWhatsappLine.numero;
            this.supWhatsappLineForm.identificador = this.supWhatsappLine.identificador;
            this.supWhatsappLineForm.es_verificado = this.supWhatsappLine.es_verificado;
            this.supWhatsappLineForm.token_validacion = this.supWhatsappLine.token_validacion;
            this.supWhatsappLineForm.destino = this.supWhatsappLine.destino;
            this.supWhatsappLineForm.tipo_de_destino = this.supWhatsappLine.tipo_de_destino;
            this.supWhatsappLineForm.mensaje_bienvenida = this.supWhatsappLine.mensaje_bienvenida;
            this.supWhatsappLineForm.mensaje_despedida = this.supWhatsappLine.mensaje_despedida;
        },
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        getDestinations () {
            this.destinationsByType = this.supWhatsappLineForm.tipo_de_destino !== null ? this.destinations[`${this.supWhatsappLineForm.tipo_de_destino}`] : [];
        },
        async save (isFormValid) {
            this.submitted = true;
            if (!isFormValid) {
                return null;
            }
            var response = null;
            if (this.formToCreate) {
                response = await this.createWhatsappLine(
                    this.supWhatsappLineForm
                );
            } else {
                response = await this.updateWhatsappLine({
                    id: this.supWhatsappLine.id,
                    data: this.supWhatsappLineForm
                });
            }
            const { status, message } = response;
            if (status === 'SUCCESS') {
                await this.initWhatsappLines();
                this.$router.push({ name: 'supervisor_whatsapp_lines' });
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
            this.closeModal();
        }
    },
    watch: {
        supWhatsappLine: {
            handler () {
                if (this.supWhatsappLine) {
                    this.initFormData();
                }
            },
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
