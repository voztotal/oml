<template>
    <div>
        <Header />
        <ListMessages />
    </div>
</template>

<script>
import Header from '@/components/agent/whatsapp/Header';
import ListMessages from '@/components/agent/whatsapp/messages/ListMessages';
export default {
    components: {
        Header,
        ListMessages
    }
};
</script>
