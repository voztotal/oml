<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h1>{{ $tc("globals.whatsapp.line", 2) }}</h1>
      </template>
    </Toolbar>
    <LinesTable @handleModalEvent="handleModal" />
    <ModalToHandleLine
      :showModal="showModal"
      :formToCreate='formToCreate'
      @handleModalEvent="handleModal" />
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import LinesTable from '@/components/supervisor/whatsapp/lines/LinesTable';
import ModalToHandleLine from '@/components/supervisor/whatsapp/lines/ModalToHandleLine';

export default {
    data () {
        return {
            showModal: false,
            formToCreate: false
        };
    },
    components: {
        LinesTable,
        ModalToHandleLine
    },
    async created () {
        await this.initWhatsappLines();
        await this.initWhatsappProviders();
    },
    methods: {
        handleModal ({ showModal = false, formToCreate = false, line = null }) {
            this.showModal = showModal;
            this.formToCreate = formToCreate;
            this.initWhatsappLine({ line });
        },
        ...mapActions(['initWhatsappLine', 'initWhatsappLines', 'initWhatsappProviders'])
    }
};
</script>
