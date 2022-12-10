<script setup>
import Pie from './components/pieChart'
import '@formkit/themes/genesis'
import axios from 'axios'
import Toggle from '@vueform/toggle'

// variables
const audioFile = ref(null);
const sortedData = ref([]);
const showLoading = ref(false);
const method = ref("1");
const chartOptions = ref({
  hoverBorderWidth: 12
});

const chartData = ref({
  hoverBackgroundColor: "red",
  hoverBorderWidth: 10,
  labels: ["Not selected"],
  datasets: [
    {
      label: "Data One",
      backgroundColor: ["#41B883", "#E46651", "#2bcb4d", "#8a4e1d", "#461aa1", "#84198c"],
      borderColor: '#dedede',
      data: [1]
    }
  ]
});

// functions
function toggleShowLoading() {
  showLoading.value = !showLoading.value
}

function handleFileUpload(event) {
  audioFile.value = event.target.files[0];
  console.log(audioFile)
}

function getPrediction() {
  let formData = new FormData();
  formData.append('audio', audioFile.value[0].file);
  formData.append('method', method.value);
  console.log(audioFile.value[0].file)

  toggleShowLoading();

  axios.post('http://127.0.0.1:5000',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
  ).then(response => {
    toggleShowLoading();
    let data = response.data
    // console.log(Object.keys(data).sort(function(a,b){return data[b]-data[a]}).map((key) => ({ [key]: data[key] })));
    data = Object.keys(data).sort((a, b) => data[b] - data[a]).reduce((r, k) => ({...r, [k]: data[k]}), {});
    // console.log(Object.entries(data).sort((a, b) => b[1] - a[1]))
    sortedData.value = data
    chartData.value.labels = Object.keys(sortedData.value);
    chartData.value.datasets[0].data = Object.values(sortedData.value);

  }).catch(error => {
    console.log(error);
  });
}

</script>

<template>
  <div class="bg-img flex flex-col">
    <div class="text-center">
      <h1>Audio classification</h1>
    </div>

    <div class="text-center mt-12">
      <FormKit :actions="false" #default="{ state: { valid } }" type="form" :submit-attrs="{ wrapperClass: 'm-auto'}"
               @submit="getPrediction">
        <FormKit
            validation="required"
            :wrapper-class="{
            'm-auto': true
          }"
            ref="file"
            v-model="audioFile"
            type="file"
            label="Audio file"
        />
        <Toggle class="mb-4" v-model="method" falseValue="Song-wise Mfccs" trueValue="Centroid Mfccs"/>
        {{ method }}
        <FormKit :wrapper-class="{
            'm-auto': true
          }" type="submit" :disabled="!valid"/>
      </FormKit>
    </div>

    <div class="text-center box-card mx-auto max-w-full">
      <div class="flex h-full">
        <div v-if="chartData.labels[0] === 'Not selected' && !showLoading" class="m-auto">
          <h1>Audio not submitted</h1>
        </div>
        <div v-else class="m-auto">
          <!-- loading button -->
          <div v-if="showLoading" class="spinner"></div>
          <!-- pie chart -->
          <div v-if="!showLoading" class="flex">
            <Pie :chartData="chartData" :chartOptions="chartOptions" :width="450"></Pie>
            <section class="ml-24 m-auto">
              <div class="flex flex-row">
              </div>
              <h1>Classified as: {{ Object.keys(sortedData)[0] }}</h1>
              <div v-for="(sortedKey, sortedVal) in Object.entries(sortedData).filter((key,index) => index < 3)">
                <span>{{ sortedKey[0] }} - {{ parseFloat(sortedKey[1]).toFixed(2) }}%</span>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  display: block;
  font-size: 2em;
  margin-top: 0.67em;
  margin-bottom: 0.67em;
  margin-left: 0;
  margin-right: 0;
  font-weight: bold;
}

.box-card {
  box-shadow: 16px 61px 45px -15px rgba(0, 0, 0, 0.1);
  background-color: #dedede;
  border-color: transparent;
  border-radius: 2rem;
  min-height: 55%;
  min-width: 60%;
  margin: auto;
}

.bg-img {
  width: 100vw;
  height: 100vh;

  background: url("static/bg5.png");
  background-size: cover;
}

.spinner {
  width: 12rem;
  height: 12rem;
  border-radius: 50%;
  background: radial-gradient(farthest-side, #8586c1 94%, #0000) top/9px 9px no-repeat,
  conic-gradient(#0000 30%, #8586c1);
  -webkit-mask: radial-gradient(farthest-side, #0000 calc(100% - 9px), #000 0);
  animation: spinner-c7wet2 1s infinite linear;
}

@keyframes spinner-c7wet2 {
  100% {
    transform: rotate(1turn);
  }
}
</style>
<style src="@vueform/toggle/themes/default.css"></style>