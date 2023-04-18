<template>
  <div>
    <Toast />
    <FileUpload
      :multiple="multiple"
      :customUpload="customUpload"
      :maxFileSize="maxFileSize"
      :fileLimit="fileLimit"
      :accept="getFileType()"
      @select="onSelectedFiles($event)"
      @uploader="customUploader($event)"
      @upload="fileUploaded($event)"
      @error="errorToUpload($event)"
      @remove="removeEvent($event)"
      @clear="clearEvent()"
      :invalidFileLimitMessage="$t('globals.media.uploaderForm.invalid_file_limit_message', {num: fileLimit})"
      :invalidFileSizeMessage="$t('globals.media.uploaderForm.invalid_file_size_message', {num: maxFileSize})"
      :invalidFileTypeMessage="$t('globals.media.uploaderForm.invalid_file_type_message')"
      :cancelLabel="$t('globals.cancel')"
      :chooseLabel="$t('globals.select')"
      :uploadLabel="$t('globals.upload')"
    >
      <template #empty>
        <div class="flex align-items-center justify-content-center flex-column">
          <i
            class="pi pi-cloud-upload border-2 border-circle p-5 text-6xl text-400 border-400"
          />
          <p class="mt-4 mb-0">{{ $t('globals.media.uploaderForm.drag_and_drop') }}</p>
        </div>
      </template>
    </FileUpload>
  </div>
</template>

<script>
export default {
    props: {
        fileType: {
            type: String,
            default: 'img'
        },
        multiple: {
            type: Boolean,
            default: false
        },
        customUpload: {
            type: Boolean,
            default: true
        },
        maxFileSize: {
            type: Number,
            default: 1000000
        },
        fileLimit: {
            type: Number,
            default: 1
        }
    },
    data () {
        return {
            files: [],
            totalSize: 0,
            totalSizePercent: 0
        };
    },
    methods: {
        getFileType () {
            return this.fileType === 'img' ? 'image/*' : 'application/pdf';
        },
        onSelectedFiles (event) {
            this.files = event.files;
            this.files.forEach((file) => {
                this.totalSize += parseInt(this.formatSize(file.size));
            });
        },
        async customUploader ($event) {
            console.log('customUploader');
            const file = this.files[0];
            console.log(file);
            const reader = new FileReader();
            const blob = await fetch(file.objectURL).then((r) => r.blob());
            reader.readAsDataURL(blob);
            // reader.onloadend = function () {
            //     const base64data = reader.result;
            // };
            this.clearData();
            this.$toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
        },
        clearData () {
            this.files = [];
            this.totalSize = 0;
            this.totalSizePercent = 0;
        },
        errorToUpload ($event) {
            console.log('Error to upload file');
            console.log($event);
        },
        clearEvent () {
            console.log('Clear Event');
        },
        removeEvent ($event) {
            console.log('Remove file');
            console.log($event);
        },
        formatSize (bytes) {
            if (bytes === 0) {
                return '0 B';
            }
            const k = 1000;
            const dm = 3;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));

            return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
        }
    }
};
</script>
