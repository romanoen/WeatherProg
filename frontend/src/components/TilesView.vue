<template>
  <div class="TilesView">
  </div>
  <div>
    <v-data-table
      v-if="apiData.length > 0"
      :headers="tableHeaders"
      :items="apiData"
      class="elevation-1"
      :items-per-page="10"
    ></v-data-table>
  </div>


  <div class = "loadingCircle">
    <v-progress-circular
    v-if="apiData.length <= 0"
    color="blue-lighten-3"
    indeterminate
    :size="156"
    :width="15"
></v-progress-circular>
  </div>
</template>
  
<script>
export default {
  name: "TilesView",
  data() {
    return {
      startDate: null,
      apiData: [], // Zum Speichern der API-Daten
      tableHeaders: [
        { title: 'Date', value: 'ds', align: 'center', sortable: true},
        { title: 'Max Temperature (C°)', value: 'temperature_2m_max', align: 'center' },
        { title: 'Min Temperature (C°)', value: 'temperature_2m_min', align: 'center' },
        { title: 'Sunshine (hours)', value: 'sunshine_duration', align: 'center' },
        { title: 'Rain (mm)', value: 'rain_sum', align: 'center' },
        { title: 'Snowfall (cm)', value: 'snowfall_sum', align: 'center' },
        { title: 'Max Wind Speed (km/h)', value: 'wind_speed_10m_max', align: 'center' },
      ],

    };
  },
  props: {
    years: Number,
    date: Date,
    today: Date,
    lat: Number,
    long: Number,
  },
  computed: {
    formattedStartDate() {
      const todayDate = new Date(this.today); // Konvertiert `today` zu einem Date-Objekt, falls nötig
      todayDate.setFullYear(todayDate.getFullYear() - this.years);
      return todayDate.toISOString().split('T')[0]; // Format YYYY-MM-DD
    },
    formattedToday() {
      const todayDate = new Date(this.today); // Konvertiert `today` zu einem Date-Objekt, falls nötig
      return todayDate.toISOString().split('T')[0]; // Format YYYY-MM-DD
    },
    periods() {
    const startDate = new Date(this.date);
    const endDate = new Date(this.today);
    const diffTime = Math.abs(endDate - startDate); // Berechnet die Differenz in Millisekunden
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // Konvertiert die Differenz in Tage
    return diffDays; // Gibt die Anzahl der Tage zurück
  },
    apiUrl() {
      const baseUrl = "http://127.0.0.1:5000/get-data";
      const endDate = this.formattedToday; // Verwendet `formattedToday`, die das Datum korrekt formatiert
      const startDate = this.formattedStartDate; // Verwendet `formattedStartDate` für das korrekte Startdatum
      const periods = this.periods;
      const latitude = this.lat;
      const longitude = this.long;
      const hourlyParameters = "rain";
      const dailyParameters = "sunshine_duration,rain_sum,snowfall_sum,wind_speed_10m_max,temperature_2m_max,temperature_2m_min,precipitation_sum";
      const dataSelector = 2;
      console.log(`${baseUrl}/${startDate}/${endDate}/${periods}/${latitude}/${longitude}/${hourlyParameters}/${dailyParameters}/${dataSelector}`)
      return `${baseUrl}/${startDate}/${endDate}/${periods}/${latitude}/${longitude}/${hourlyParameters}/${dailyParameters}/${dataSelector}`;
    }
  },

  watch: {
    formattedStartDate(newVal) {
      this.startDate = newVal;
    },
  },
  methods: {
  async fetchdata() {
    try {
      const response = await fetch(this.apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.apiData = await response.json();
      this.roundApiDataValues();
      console.log("API Response:", this.apiData[0].temperature_2m_max); // Gibt die API-Antwort in der Konsole aus
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  },
  roundApiDataValues() {
      this.apiData = this.apiData.map(dataItem => ({
        ...dataItem,
        ds: dataItem.ds.substring(0, dataItem.ds.indexOf('00:00:00')).trim(), // Entfernt den Zeitanteil und das letzte Leerzeichen
        temperature_2m_max: Math.round(dataItem.temperature_2m_max),
        temperature_2m_min: Math.round(dataItem.temperature_2m_min),
        sunshine_duration: Math.round(dataItem.sunshine_duration/3600),
        rain_sum: Math.round(dataItem.rain_sum),
        snowfall_sum: Math.round(dataItem.snowfall_sum),
        wind_speed_10m_max: Math.round(dataItem.wind_speed_10m_max),
        // Fügen Sie hier ggf. weitere zu rundende Felder hinzu
      }));
    }
  },
  mounted() {
  }
}

</script>
  
<style>
.TilesView {
  background-color: rgb(251, 251, 152);
}

.loadingCircle {
  margin-top: 15em;
}


</style>
