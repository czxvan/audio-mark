<template>
  <FileUpload
    ref="fileUpload"
    name="file"
    mode="advanced"
    url="http://127.0.0.1:8000/api/detect/upload"
    accept=".wav"
    :auto="false"
    :multiple="true"
    :with-credentials="true"
    :files="files" 
    @select="onSelect"
    @upload="onUpload"
    class="file-upload"
  >
    <template #empty>
      <div class="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg">
        <i class="pi pi-cloud-upload text-4xl text-gray-400 mb-4"></i>
        <p class="text-gray-600">Drag and drop wav audio files here to upload.</p>
      </div>
    </template>
  </FileUpload>

  <TabMenu :model="items" class="mt-6" />

  <div v-if="audioSrc[activeIndex] && imageSrc[activeIndex]" class="mt-6 flex flex-col items-center">
    <div class="flex items-center">
      <div v-if="audioSrc[activeIndex] && imageSrc[activeIndex]" class="flex flex-col items-center">
        <audio :src="audioSrc[activeIndex]" controls class="w-full max-w-4xl rounded-lg shadow-lg border border-gray-200"></audio>
        <img :src="imageSrc[activeIndex]" alt="Spectrogram" class="mt-6 w-full max-w-8xl rounded-lg shadow-lg border border-gray-200" />
      </div>
      <div class="text-lg font-semibold ml-6 mt-12 p-4 flex flex-col bg-white rounded-lg shadow-lg border border-gray-200">
        <h2 class="text-center mb-4 text-2xl text-blue-600">Detect Result</h2>
        <p class="mb-2 flex">•&nbsp;<span class="font-bold w-1/2">File Name:</span> <span class="text-blue-500">{{ filename }}</span></p>
        <p class="mb-2 flex">•&nbsp;<span class="font-bold w-1/2">Probability:</span> <span class="text-blue-500">{{ results[activeIndex].toFixed(2) }}</span></p>
        <p class="mb-2 flex">•&nbsp;<span class="font-bold w-1/2">Message String:</span> <span class="text-blue-500">{{ messages_s[activeIndex] }}</span></p>
        <p class="mb-2">•&nbsp;<span class="font-bold">Message Tensor:</span><br><span class="text-blue-500">{{ messages[activeIndex] }}</span></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FileUpload from 'primevue/fileupload';
import TabMenu from 'primevue/tabmenu';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const files = ref([]);
const fileUpload = ref(null);
const audioSrc = ref(['', '', '']);
const imageSrc = ref(['', '', '']);
const filename = ref('');
const results = ref([0, 0, 0]);
const messages = ref([null, null, null]);
const messages_s = ref(['', '', '']);
const activeIndex = ref(0);

const items = ref([
    { label: 'Potential Watermarked Audio', command: () => { activeIndex.value = 0 } },
    { label: 'Pink Noised Audio', command: () => { activeIndex.value = 1 } },
    { label: 'Losspass Filtered Audio', command: () => { activeIndex.value = 2 } },
]);

const onSelect = (event) => {
  // [TODO] hope remove completeed files when choose new files
  fileUpload.value.files = [event.files[event.files.length - 1]];
};

const onUpload = async (event) => {
  await Promise.all([detectAudio(), detectPinkNoisedAudio(), detectLowpassFilteredAudio()]);
  toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'Your files have been uploaded successfully.', life: 3000 });
  filename.value = event.files[0].name;
};

async function getDetectResult(url) {
  try {
    const response = await fetch('http://127.0.0.1:8000' + url, {
       credentials: 'include'
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting audio figure:', error);
  }
};

async function detectAudio() {
  const {audio, figure, result, message, message_s} = await getDetectResult('/api/detect/audio');
  audioSrc.value[0] = audio;
  imageSrc.value[0] = figure;
  results.value[0] = result;
  messages.value[0] = message;
  messages_s.value[0] = message_s;
};

async function detectPinkNoisedAudio() {
  const {audio, figure, result, message, message_s} = await getDetectResult('/api/detect/pink-noised-audio');
  audioSrc.value[1] = audio;
  imageSrc.value[1] = figure;
  results.value[1] = result;
  messages.value[1] = message;
  messages_s.value[1] = message_s;
};

async function detectLowpassFilteredAudio() {
  const {audio, figure, result, message, message_s} = await getDetectResult('/api/detect/lowpass-filtered-audio');
  audioSrc.value[2] = audio;
  imageSrc.value[2] = figure;
  results.value[2] = result;
  messages.value[2] = message;
  messages_s.value[2] = message_s;

};

</script>

<style scoped>
/* Add any custom styles here */
</style>