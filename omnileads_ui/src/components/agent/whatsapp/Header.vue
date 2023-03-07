<template>
  <div class="card">
    <Toolbar class="mb-4">
      <template #start>
        <p>Whatsapp</p>
      </template>
      <template #end>
        <Button
        icon="pi pi-search"
        class="p-button-rounded p-button-info ml-2"
        @click="search"
        v-tooltip.top="'Buscar conversarion'"
        />

        <Button
        icon="pi pi-comment"
        class="p-button-rounded ml-2"
        @click="newConversation"
        v-tooltip.top="'Nueva conversarion'"
        />
      </template>
    </Toolbar>
  </div>
</template>

<script>
export default {
    methods: {
        search () {
        },
        newConversation () {}
    }
};
</script>
