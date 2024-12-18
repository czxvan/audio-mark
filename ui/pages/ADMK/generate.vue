<template>
  <div>
    <FileUpload
      ref="fileUpload"
      name="file"
      mode="advanced"
      url="http://127.0.0.1:8000/api/generate/upload"
      accept=".wav"
      :auto="false"
      :multiple="true"
      :with-credentials="true"
      :files="files" 
      @select="onSelect"
      @upload="onUpload"
    >
      <template #empty>
          <div class="flex items-center justify-center flex-col">
              <i class="pi pi-cloud-upload !border-2 !rounded-full !p-3 !text-4xl !text-muted-color" />
              <p class="mt-6 mb-0">Drag and drop wav audio to here to upload.</p>
          </div>
      </template>
    </FileUpload>
    <div class="mt-5 flex gap-2 items-center gap-5">
      <label class="block text-gray-600 text-lg font-bold mb-1 ml-3">Message:</label>
      <InputText v-model="message" type="text" placeholder="CM"/>
      <Button label="Regenerate" @click="regenerate" />
    </div>
  </div>

  <TabMenu :model="items" class="mt-6" />

  <div v-if="audioSrc[activeIndex] && imageSrc[activeIndex]" class="mt-6 flex flex-col items-center">
    <audio :src="audioSrc[activeIndex]" controls class="w-full max-w-3xl rounded-lg shadow-lg border border-gray-200"></audio>
    <img :src="imageSrc[activeIndex]" alt="Spectrogram" class="mt-6 w-full max-w-7xl rounded-lg shadow-lg border border-gray-200" />
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
const message = ref('');
const activeIndex = ref(0);

const items = ref([
    { label: 'Original Audio', command: () => { activeIndex.value = 0 } },
    { label: 'WaterMark', command: () => { activeIndex.value = 1 } },
    { label: 'Watermarked Audio', command: () => { activeIndex.value = 2 } },
]);

const onSelect = (event) => {
  // [TODO] hope remove completeed files when choose new files
  fileUpload.value.files = [event.files[event.files.length - 1]];
};

const onUpload = async (event) => {
  await Promise.all([generateAudio(), generateWatermark(), generateWatermarkedAudio()]);
  toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'Your files have been uploaded successfully.', life: 3000 });
};

async function getAudioFigure(url) {
  try {
    const response = await fetch('http://127.0.0.1:8000'+url,{
       credentials: 'include'
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting audio figure:', error);
  }
};

async function generateAudio() {
  const {audio, figure} = await getAudioFigure('/api/generate/audio');
  audioSrc.value[0] = audio;
  imageSrc.value[0] = figure;
};

async function generateWatermark() {
  const {audio, figure} = await getAudioFigure('/api/generate/watermark/' + message.value);
  console.log('message:', message.value);
  audioSrc.value[1] = audio;
  imageSrc.value[1] = figure;
};

async function generateWatermarkedAudio() {
  const {audio, figure} = await getAudioFigure('/api/generate/watermarked-audio/' + message.value);
  audioSrc.value[2] = audio;
  imageSrc.value[2] = figure;
};

async function regenerate() {
  await Promise.all([generateWatermark(), generateWatermarkedAudio()]);
  toast.add({ severity: 'success', summary: 'Regenerate Successful', detail: 'The message is: ' + message.value, life: 3000 });

};

</script>

<style scoped>
/* Add any custom styles here */
</style>