<template>
  <div>
    <HeaderMediaUploader @handleCloseEvent="closeEvent" />
    <MediaUploader ref="mediaFormRef" :fileType="fileType" />
  </div>
</template>

<script>
import HeaderMediaUploader from '@/components/agent/whatsapp/conversation/HeaderMediaUploader';
import MediaUploader from '@/components/agent/whatsapp/shared/media/MediaUploader';
export default {
    components: {
        HeaderMediaUploader,
        MediaUploader
    },
    methods: {
        closeEvent () {
            this.$refs.mediaFormRef.clearData();
        }
    },
    data () {
        return {
            fileType: 'img'
        };
    },
    created () {
        const element = window.parent.document.getElementById(
            'agentWhatsMediaFormType'
        );
        element.addEventListener('input', (e) => {
            console.log('Input change value');
            console.log(e.target);
        });
        this.fileType = element?.value || 'img';
    }
};
</script>
