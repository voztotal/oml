<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h1>{{ $tc("globals.form", 2) }}</h1>
      </template>
      <template #end>
        <Button
          :label="$tc('globals.new')"
          icon="pi pi-plus"
          @click="newForm"
        />
      </template>
    </Toolbar>
    <ProvidersTable />
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import ProvidersTable from '@/components/supervisor/whatsapp/providers/ProvidersTable';

export default {
    components: {
        ProvidersTable
    },
    async created () {
        await this.initWhatsappProviders();
    },
    methods: {
        newForm () {
            this.$router.push({ name: 'supervisor_forms_new_step1' });
        },
        ...mapActions(['initWhatsappProviders'])
    }
};
</script>
