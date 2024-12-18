<template>
  <div class="card">
    <Toast />
    <FileUpload
      name="file"
      url="http://localhost:8000/api/flowgraph/upload_zip" <!-- 指向 FastAPI 后端的上传接口 -->
      @upload="onAdvancedUpload($event)"
      :multiple="true"
      accept=".zip"
      :maxFileSize="100000000"
    >
      <template #empty>
        <span>Drag and drop files to here to upload.</span>
      </template>
    </FileUpload>
  </div>
</template>

<script setup>
</script>
