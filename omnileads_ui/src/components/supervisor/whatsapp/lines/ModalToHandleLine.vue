<template>
  <Dialog
    :visible="showModal"
    :style="{ width: '50vw' }"
    :closable="false"
    :modal="false"
  >
    <template #header>
      <h2>{{ formToCreate ? $t("views.whatsapp.line.new_title") : $t("views.whatsapp.line.edit_title") }}</h2>
    </template>
    <Form @closeModalEvent="closeModal" :formToCreate="formToCreate" />
  </Dialog>
</template>

<script>
import { mapActions } from 'vuex';
import Form from '@/components/supervisor/whatsapp/lines/Form';

export default {
    props: {
        showModal: {
            type: Boolean,
            default: false
        },
        formToCreate: {
            type: Boolean,
            default: true
        }
    },
    components: {
        Form
    },
    methods: {
        ...mapActions(['initWhatsappLine']),
        closeModal () {
            this.$emit('handleModalEvent', {});
            this.initWhatsappLine({});
        }
    }
};
</script>
