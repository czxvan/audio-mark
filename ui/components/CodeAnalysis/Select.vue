
<template>
    <div class="card flex justify-center">
        <Select v-model="selectedFile" editable :options="files" optionLabel="name" placeholder="Select a File" class="w-full md:w-56" />
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// 响应式数据
const selectedFile = ref(null);
const files = ref([]);

// 获取城市列表的函数
const fetchFiles = async () => {
  try {
    // 向后端请求数据
    const response = await axios.get("http://localhost:8000/files");
    files.value = response.data;  // 将返回的数据赋值给 files
  } catch (error) {
    console.error("Error fetching files:", error);
  }
};

// 在组件挂载时获取城市列表
onMounted(() => {
    fetchFiles();
});
</script>