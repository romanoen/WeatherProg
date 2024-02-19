<template>
    <link href="https://cdn.jsdelivr.net/npm/@mdi/font/css/materialdesignicons.min.css" rel="stylesheet">

    <div class="overview">
        <div class="navbar">
            <p class="weatherprog">
                WeatherProg
            </p>
            <img src="/earth2.svg" alt="Weather Icon" class="weathericon">
        </div>
        <div class="utilities">

            <div class="searchbar">
                <v-text-field id="autocomplete" v-model="searchQuery" label="Search Location" placeholder="Münster"
                    variant="solo" rounded :clearable=true prepend-inner-icon="mdi-map-marker"></v-text-field>
                <button @click="formatDate(selectedDate)">printAdress</button>
                <button @click="printPlace()">GaGa</button>
            </div>

            <div class="datefield">
                <div>
                    <v-text-field @click="toggleDatePicker()" v-model="selectedDate" label="Select Date" readonly
                        variant="solo" rounded class="date-picker-field"
                        prepend-inner-icon="mdi-calendar-text"></v-text-field>
                </div>

                <div class="datepicker">
                    <v-menu v-model="showDatePicker" :close-on-content-click=false>
                        <v-date-picker v-if="showDatePicker" v-model="selectedDate" color="rgb(128, 0, 128)"
                            class="datepicker" :min="today"></v-date-picker>
                    </v-menu>
                </div>
            </div>

            <div class="yearpicker">
                <v-text-field v-model="years" type="number" label="Years" variant="solo" rounded :max="20"></v-text-field>
            </div>

            <div class=okButtonDiv>
                <v-btn block rounded="xl" size="x-large" color="green" @click="printAll()"><i
                        class="mdi mdi-check"></i></v-btn>
            </div>
        </div>
    </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
export default {
    data() {
        return {
            searchQuery: '',
            place: null,
            geocoder: new window.google.maps.Geocoder(),
            showDatePicker: false,
            years: 3,
            selectedDate: new Date(), // Initialize selectedDate here
            today: new Date() 
        }
    },
    mounted() {
        var input = document.getElementById("autocomplete");
        // eslint-disable-next-line no-unused-vars
        var autocomplete = new window.google.maps.places.Autocomplete(input);
        autocomplete.addListener('place_changed', () => {
            this.searchQuery = input.value;
            this.geocodeAddress(this.searchQuery);
        });
    },


    methods: {

        printAddress() {
            console.log(this.searchQuery);
        },

        printPlace() {
            console.log(this.place.lat, this.place.lng)
        },

        geocodeAddress(address) {
            this.geocoder.geocode({ 'address': address }, (results, status) => {
                if (status === 'OK') {
                    const location = results[0].geometry.location;
                    // Assuming the API returns a location object with lat() and lng() methods
                    this.place = {
                        lat: location.lat(), // Retrieve the latitude
                        lng: location.lng() // Retrieve the longitude
                    };

                } else {
                    console.log('Geocode war nicht erfolgreich aus folgendem Grund: ' + status);
                }
            });
        },

        toggleDatePicker() {
            this.showDatePicker = !this.showDatePicker;
        },

        formatDate(date) {
            let year = date.getFullYear();
            let month = (date.getMonth() + 1).toString().padStart(2, '0'); // Monate sind von 0-11
            let day = date.getDate().toString().padStart(2, '0');
            console.log(`${year}-${month}-${day}`)
            return `${year}-${month}-${day}`;
        },

        printAll() {
            console.log(this.searchQuery)
            console.log(this.place.lat, this.place.lng)
            console.log(this.today)
            console.log(this.selectedDate)
            console.log(this.years)
        }
    }

}
</script>

<script setup>
//import { ref } from 'vue'
//const selectedDate = ref(new Date()) 
//const today = ref(new Date())


</script>

<style>
.navbar {
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    background: linear-gradient(to right, rgb(255, 255, 255) 0%, rgb(189, 142, 189) 33%, rgb(189, 142, 189) 33%, rgb(128, 0, 128) 100%);
    text-align: left;
    color: black;
    display: flex;

}

.weatherprog {
    font-size: x-large;
    font-weight: 600;
    padding-left: 0.5em;
    margin-top: 1em;
}

.weathericon {
    width: 195px;
    /* oder jede andere Größe, die Sie bevorzugen */
    height: 195px;
    /* oder jede andere Größe, die Sie bevorzugen */
    margin-right: 8px;
    margin-top: -55px;
    margin-bottom: -55px;
    margin-left: -20px;
}

.overview {
    display: flex;
    flex-direction: column;
}

.utilities {
    display: flex;
    justify-content: center;
    flex-direction: row;
    margin-top: 2em;
}

.searchbar {
    width: 40em;
}

.datefield {
    width: 11.5em;
    cursor: pointer;
    margin-left: 1.5em;
}

.date-picker-field * {
    cursor: pointer !important;
}


.datepicker {
    position: relative;
    left: 80em;
    top: 10em;
}

.yearpicker {
    margin-left: 1.5em;
    width: 5em;
}

.okButtonDiv {
    margin-left: 1.5em;
}
</style>