<template>
  <TabView class="tabview-custom">
    <TabPanel>
      <template #header>
        <i class="pi pi-list mr-2"></i>
        <span>{{ $t('views.whatsapp.management_form.form') }}</span>
      </template>
      <Form ref="formRef"/>
    </TabPanel>
    <TabPanel>
      <template #header>
        <i class="pi pi-history mr-2"></i>
        <span>{{ $t('views.whatsapp.management_form.record') }}</span>
      </template>
      <Historial />
    </TabPanel>
  </TabView>
</template>

<script>
import Form from '@/components/agent/whatsapp/management_form/Form';
import Historial from '@/components/agent/whatsapp/management_form/Historial';
export default {
    components: {
        Form,
        Historial
    },
    methods: {
        closeEvent () {
            this.$refs.formRef.resetData();
        }
    }
};
</script>
