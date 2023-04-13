<template>
  <div>
    <Header />
    <Form />
  </div>
</template>

<script>
import Header from '@/components/agent/whatsapp/message_transfer/Header';
import Form from '@/components/agent/whatsapp/message_transfer/Form';
import { mapActions } from 'vuex';
export default {
    components: {
        Header,
        Form
    },
    methods: {
        ...mapActions(['agtWhatsManagementInitData'])
    },
    created () {
        this.agtWhatsManagementInitData();
    }
};
</script>
