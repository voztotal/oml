<template>
  <Toolbar>
    <template #start>
      <Button
        @click="back"
        v-tooltip.top="'Regresar'"
        icon="pi pi-arrow-left"
        class="p-button-rounded p-button-secondary p-button-text"
      />
      <Chip
        label="Amy Elsner"
        image="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png"
      />
    </template>
    <template #end>
      <SplitButton
        @click="attach"
        icon="pi pi-paperclip"
        :model="attachOptions"
        v-tooltip.top="'Adjuntar'"
        class="p-button-warning"
      />
      <Button
        icon="pi pi-copy"
        class="p-button-info ml-2"
        @click="templates"
        v-tooltip.top="'Plantillas'"
      />
      <Button
        icon="pi pi-save"
        class="ml-2"
        @click="save"
        v-tooltip.top="'Guardar'"
      />
      <Button
        icon="pi pi-arrows-h"
        class="p-button-secondary ml-2"
        @click="transfer"
        v-tooltip.top="'Transferir'"
      />
    </template>
  </Toolbar>
</template>

<script>
export default {
    data () {
        return {
            attachOptions: [
                {
                    label: 'Imagenes',
                    icon: 'pi pi-image',
                    command: () => {}
                },
                {
                    label: 'Documentos',
                    icon: 'pi pi-file-pdf',
                    command: () => {}
                }
            ]
        };
    },
    methods: {
        back () {
            this.$router.push({ name: 'agent_whatsapp' });
        },
        templates () {},
        attach () {},
        save () {},
        transfer () {}
    }
};
</script>
