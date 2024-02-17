<template>
    <div class = "navbar">
        <p class = "weatherprog">
            WeatherProg
        </p>
        <img src="..\assets\earth2.svg" alt="Weather Icon" class = "weathericon">
    </div>
</template>

<script>
</script>

<style>
.navbar{
    width: 100%; 
    position: fixed; 
    top: 0; 
    left: 0; 
    background: linear-gradient(to right, rgb(255, 255, 255) 0%, rgb(189, 142, 189) 33%, rgb(189, 142, 189) 33%, rgb(128, 0, 128) 100%); 
    text-align: left; 
    color: black;
    display: flex;
    
}

.weatherprog{
    font-size: x-large;
    font-weight: 600;
    padding-left: 0.5em;
}

.weathericon{
    width: 195px; /* oder jede andere Größe, die Sie bevorzugen */
    height: 195px; /* oder jede andere Größe, die Sie bevorzugen */
    margin-right: 8px;
    margin-top: -55px;
    margin-bottom: -55px;
    margin-left: -20px;
}

</style>