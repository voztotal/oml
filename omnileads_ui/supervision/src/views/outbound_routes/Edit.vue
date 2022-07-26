<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h1>{{ $t("forms.outbound_route.edit_outbound_route") }}</h1>
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
    <Form :outboundRoute="outboundRouteDetail" :formToCreate="false" />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import Form from '@/components/outbound_routes/Form';

export default {
    components: {
        Form
    },
    async created () {
        const id = this.$route.params.id;
        await this.initOutboundRouteDetail(id);
        await this.initOutboundRouteForm(this.outboundRouteDetail);
    },
    methods: {
        ...mapActions(['initOutboundRouteDetail', 'initOutboundRouteForm']),
        backToOutboundRoutesList () {
            this.$router.push({ name: 'outbound_routes' });
        }
    },
    computed: {
        ...mapState(['outboundRouteDetail'])
    }
};
</script>
