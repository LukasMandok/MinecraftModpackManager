<template>
  <div class="about">
    <h1>This is an about page</h1>
    <div>
      <span>There will be a very nice button</span>
      <button @click="requestDownloadList">Request Download List</button>
    </div>
  </div>
</template>

<script>
  export default {
    methods: {
      requestDownloadList() {
        window.eel.request_download_list()(); // Call the Eel function
      }
    }
  }
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
