<template>
  <div>
    <div class="flex justify-content-between flex-wrap">
      <div class="flex align-items-center justify-content-center">
        <Avatar
          image="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png"
          size="large"
          shape="circle"
        />
        <span class="pl-2">{{ name }}</span>
      </div>
      <div class="flex align-items-center justify-content-center">
        <Badge value="4" severity="success" />
      </div>
    </div>
    <div class="flex justify-content-end flex-wrap">
      <div class="flex align-items-center justify-content-center">
        <small class="font-italic">
          {{ time }}
        </small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        name: {
            type: String,
            default: '-----'
        },
        time: {
            type: String,
            default: '-----'
        }
    }
};
</script>
