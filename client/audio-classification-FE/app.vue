<script setup>
import Pie from './components/pieChart'
import '@formkit/themes/genesis'
// variables
const audioFile = ref(null);
const showLoading = ref(false);
const chartOptions = ref({
  hoverBorderWidth: 20
});
const chartData = ref({
  hoverBackgroundColor: "red",
  hoverBorderWidth: 10,
  labels: ["Green", "Red", "Blue"],
  datasets: [
    {
      label: "Data One",
      backgroundColor: ["#41B883", "#E46651", "#00D8FF"],
      data: [1, 10, 5]
    }
  ]
});

// functions
function toggleShowLoading() {
  showLoading.value = !showLoading.value
}

function getPrediction() {

  // this.$axios.$post('http://icanhazip.com').then(response =>{
  //   console.log(response)
  // })
  toggleShowLoading();
  setTimeout(function () {
    toggleShowLoading();
  }, 5000);
}

</script>

<template>
  <div class="bg-img flex flex-col">
    <div class="text-center">
      <h1>Audio classification</h1>
    </div>

    <div class="text-center mt-12">
      <FormKit type="form" :submit-attrs="{ wrapperClass: 'm-auto'}" @submit="getPrediction">
      <FormKit
          :wrapper-class="{
            'm-auto': true
          }"
          v-model="audioFile"
          type="file"
          label="Audio file"
      />
      </FormKit>
    </div>

    <div class="text-center box-card mx-auto max-w-full">
      <div class="flex h-full">
        <!-- loading button -->
        <div v-if="showLoading" class="spinner m-auto"></div>
        <!-- pie chart -->
        <Pie class="m-auto" v-if="!showLoading" :chartData="chartData" :chartOptions="chartOptions"></Pie>
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
