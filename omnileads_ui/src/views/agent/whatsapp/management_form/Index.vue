<template>
  <div>
    <Header />
    <Tab />
  </div>
</template>

<script>
import Header from '@/components/agent/whatsapp/management_form/Header';
import Tab from '@/components/agent/whatsapp/management_form/Tab';
import { mapActions } from 'vuex';
export default {
    components: {
        Header,
        Tab
    },
    methods: {
        ...mapActions(['agtWhatsManagementInitData'])
    },
    created () {
        this.agtWhatsManagementInitData();
    }
};
</script>
