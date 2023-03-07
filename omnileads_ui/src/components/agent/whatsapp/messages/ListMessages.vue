<template>
  <Listbox
    v-model="selectedCountries"
    :options="countries"
    :filter="true"
    optionLabel="name"
    filterPlaceholder="Search"
  >
    <template #option="data">
      <ConversationInfo :name="data.option.name" :time="time" />
    </template>
  </Listbox>
</template>

<script>
import ConversationInfo from '@/components/agent/whatsapp/shared/ConversationInfo';

export default {
    components: {
        ConversationInfo
    },
    data () {
        return {
            selectedCountries: null,
            time: new Date().toLocaleString(),
            countries: [
                { name: 'Australia', code: 'AU' },
                { name: 'Brazil', code: 'BR' },
                { name: 'China', code: 'CN' },
                { name: 'Egypt', code: 'EG' },
                { name: 'France', code: 'FR' },
                { name: 'Germany', code: 'DE' },
                { name: 'India', code: 'IN' },
                { name: 'Japan', code: 'JP' },
                { name: 'Spain', code: 'ES' },
                { name: 'United States', code: 'US' }
            ]
        };
    }
};
</script>
