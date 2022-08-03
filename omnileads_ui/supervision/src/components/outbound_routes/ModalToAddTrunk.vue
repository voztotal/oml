<template>
  <Dialog
    :visible="showModal"
    :style="{ width: '35vw' }"
    :closable="false"
    :modal="true"
  >
    <template #header>
      <h2>{{ $t("views.trunk.new_title") }}</h2>
    </template>
    <div class="card">
      <div class="grid formgrid">
        <div class="field col-12">
          <label
            id="pause_type"
            :class="{
              'p-error': v$.trunk.$invalid && submitted,
            }"
            >{{ $t("globals.trunk") }}*</label
          >
          <Dropdown
            v-model="trunk"
            class="w-full mt-2"
            :class="{
              'p-invalid': v$.trunk.$invalid && submitted,
            }"
            :options="trunks"
            placeholder="-----"
            optionLabel="nombre"
            optionValue="id"
            :emptyFilterMessage="$t('globals.without_data')"
            :filter="true"
            v-bind:filterPlaceholder="
              $t('globals.find_by', { field: $tc('globals.name') }, 1)
            "
          />
          <small
            v-if="
              (v$.trunk.$invalid && submitted) || v$.trunk.$pending.$response
            "
            class="p-error"
            >{{
              v$.trunk.required.$message.replace("Value", $t("globals.trunk"))
            }}</small
          >
        </div>
      </div>
    </div>
    <template #footer>
      <div class="flex justify-content-end flex-wrap">
        <Button
          class="p-button-danger p-button-outlined mr-2"
          :label="$t('globals.cancel')"
          @click="closeModal"
        />
        <Button :label="$t('globals.save')" @click="save(!v$.$invalid)" />
      </div>
    </template>
  </Dialog>
</template>

<script>
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { mapActions } from 'vuex';

export default {
    setup: () => ({ v$: useVuelidate({ $scope: false }) }),
    validations () {
        return {
            trunk: { required }
        };
    },
    inject: ['$helpers'],
    props: {
        trunks: {
            type: Array,
            default: () => []
        },
        showModal: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            submitted: false,
            trunk: null
        };
    },
    async created () {
        await this.initializeData();
    },
    methods: {
        ...mapActions(['addTrunk']),
        initializeData () {
            this.submitted = false;
            this.trunk = null;
        },
        closeModal () {
            this.$emit('handleTrunkModalEvent', false);
            this.initializeData();
        },
        async save (isFormValid) {
            this.submitted = true;
            if (!isFormValid) {
                return null;
            }
            // const trunkId = this.trunk;
            // this.trunk = this.trunks.find((t) => t.id === trunkId);
            this.addTrunk(this.trunk);
            this.closeModal();
        }
    },
    watch: {
        trunks: {
            handler () {},
            deep: true,
            immediate: true
        }
    }
};
</script>
