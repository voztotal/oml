<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h1>{{ $t("forms.outbound_route.new_outbound_route") }}</h1>
      </template>
      <template #end>
        <Button
          :label="$tc('globals.back')"
          icon="pi pi-arrow-left"
          class="p-button-info mr-2"
          @click="backToOutboundRoutesList"
        />
      </template>
    </Toolbar>
    <Form />
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Form from '@/components/outbound_routes/Form';

export default {
    components: {
        Form
    },
    created () {
        this.initOutboundRouteForm();
    },
    methods: {
        ...mapActions(['initOutboundRouteForm']),
        backToOutboundRoutesList () {
            this.$router.push({ name: 'outbound_routes' });
        }
    }
};
</script>
