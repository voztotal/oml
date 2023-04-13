<template>
  <FileUpload
    name="demo[]"
    url="./upload.php"
    @upload="onFileUploaded($event)"
    :multiple="false"
    :accept="getFileType()"
    :customUpload="true"
    :fileLimit="1"
    :maxFileSize="1000000"
    @select="onSelectedFiles"
    @uploader="customUploader()"
    :cancelLabel="'Cancelar'"
    :chooseLabel="'Selecciona'"
    :uploadLabel="'Cargar'"
  >
    <template
      #content="{
        files,
        uploadedFiles,
        removeUploadedFileCallback,
        removeFileCallback,
      }"
    >
      <div v-if="files.length > 0">
        <h5>Pending</h5>
        <div class="flex flex-wrap p-0 sm:p-5 gap-5">
          <div
            v-for="(file, index) of files"
            :key="file.name + file.type + file.size"
            class="card m-0 px-6 flex flex-column border-1 surface-border align-items-center gap-3"
          >
            <div>
              <img
                role="presentation"
                :alt="file.name"
                :src="file.objectURL"
                width="100"
                height="50"
                class="shadow-2"
              />
            </div>
            <span class="font-semibold">{{ file.name }}</span>
            <div>{{ formatSize(file.size) }}</div>
            <Badge value="Pending" severity="warning" />
            <Button
              icon="pi pi-times"
              @click="onRemoveTemplatingFile(file, removeFileCallback, index)"
              outlined
              rounded
              severity="danger"
            />
          </div>
        </div>
      </div>

      <div v-if="uploadedFiles.length > 0">
        <h5>Completed</h5>
        <div class="flex flex-wrap p-0 sm:p-5 gap-5">
          <div
            v-for="(file, index) of uploadedFiles"
            :key="file.name + file.type + file.size"
            class="card m-0 px-6 flex flex-column border-1 surface-border align-items-center gap-3"
          >
            <div>
              <img
                role="presentation"
                :alt="file.name"
                :src="file.objectURL"
                width="100"
                height="50"
                class="shadow-2"
              />
            </div>
            <span class="font-semibold">{{ file.name }}</span>
            <div>{{ formatSize(file.size) }}</div>
            <Badge value="Completed" class="mt-3" severity="success" />
            <Button
              icon="pi pi-times"
              @click="removeUploadedFileCallback(index)"
              outlined
              rounded
              severity="danger"
            />
          </div>
        </div>
      </div>
    </template>
    <template #empty>
      <div class="flex align-items-center justify-content-center flex-column">
        <i
          class="pi pi-cloud-upload border-2 border-circle p-5 text-6xl text-400 border-400"
        />
        <p class="mt-4 mb-0">Drag and drop files to here to upload.</p>
      </div>
    </template>
  </FileUpload>
</template>

<script>
export default {
    props: {
        fileType: {
            type: String,
            default: 'img'
        }
    },
    data () {
        return {
            files: [],
            totalSize: 0,
            totalSizePercent: 0
        };
    },
    computed: {
        progressBarStatus () {
            return {
                'exceeded-progress-bar': this.totalSizePercent > 100
            };
        }
    },
    methods: {
        getFileType () {
            return this.fileType === 'img' ? 'image/*' : 'application/pdf';
        },
        onRemoveTemplatingFile (file, removeFileCallback, index) {
            removeFileCallback(index);
            this.totalSize -= parseInt(this.formatSize(file.size));
            this.totalSizePercent = this.totalSize / 10;
        },
        onClearTemplatingUpload (clear) {
            clear();
            this.totalSize = 0;
            this.totalSizePercent = 0;
        },
        onSelectedFiles (event) {
            this.files = event.files;
            this.files.forEach((file) => {
                this.totalSize += parseInt(this.formatSize(file.size));
            });
        },
        uploadEvent (callback) {
            this.totalSizePercent = this.totalSize / 10;
            callback();
        },
        async customUploader () {
            console.log('customUploader');
            const file = this.files[0];
            console.log(file);
            // const reader = new FileReader();
            // let blob = await fetch(file.objectURL).then((r) => r.blob()); //blob:url
            // reader.readAsDataURL(blob);
            // reader.onloadend = function () {
            //     const base64data = reader.result;
            // };
        },
        onFileUploaded () {
            this.$toast.add({
                severity: 'info',
                summary: 'Success',
                detail: 'File Uploaded',
                life: 3000
            });
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
