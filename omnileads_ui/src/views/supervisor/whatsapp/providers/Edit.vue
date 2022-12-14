<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h1>{{ $t("globals.edit") }} {{ $tc("globals.whatsapp.provider") }}</h1>
      </template>
      <template #end>
        <Button
          :label="$t('globals.back')"
          icon="pi pi-arrow-left"
          class="p-button-info mr-2"
          @click="back"
        />
      </template>
    </Toolbar>
    <Form :formToCreate="false" />
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Form from '@/components/supervisor/whatsapp/providers/Form';

export default {
    components: {
        Form
    },
    async created () {
        const id = this.$route.params.id;
        await this.initWhatsappProvider(id);
    },
    methods: {
        ...mapActions(['initWhatsappProvider']),
        back () {
            this.$router.push({ name: 'supervisor_whatsapp_providers' });
        }
    }
};
</script>
