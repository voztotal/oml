<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <h2 class="font-bold">Whatsapp</h2>
      </template>
      <template #end>
        <!-- <Button
        icon="pi pi-search"
        class="p-button-rounded p-button-info p-button-outlined ml-2"
        @click="search"
        v-tooltip.top="'Buscar conversarion'"
        /> -->
        <Button
        icon="pi pi-comment"
        class="p-button-secondary"
        @click="newConversation"
        v-tooltip.top="'Nueva conversarion'"
        />
        <Button
        icon="pi pi-times"
        class="p-button-danger ml-2"
        @click="close"
        v-tooltip.top="'Cerrar'"
        />
      </template>
    </Toolbar>
  </div>
</template>

<script>
export default {
    methods: {
        newConversation () {},
        search () {},
        close () {}
    }
};
</script>
