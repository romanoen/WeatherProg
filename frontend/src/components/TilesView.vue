<template>
  <div class=TilesView>
    Hallo, ich bin eine Child-Komponente! {{ years }} {{ date }} {{ today }} {{ lat }} {{ long }} {{ startDate }}
  </div>
</template>
  
<script>
export default {
  name: "TilesView",
  data(){
    startDate = null
  }
  ,
  props: {
    years: Number,
    date: Date,
    today: Date,
    lat: Number,
    long: Number
  },
  computed: {
    startingdate() {
      const startDate = new Date(this.today); // Clone the today date to avoid mutating the prop
      startDate.setFullYear(startDate.getFullYear() - this.years); // Subtract years
      this.startDate = startDate
      return startDate;
    }
  }
}
</script>
  
<style>
.TilesView {
  background-color: rgb(251, 251, 152);
}
</style>