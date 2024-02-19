// Import Vue and the main App component
import { createApp } from 'vue'
import App from './App.vue'

// Import Vuetify styles and the createVuetify function
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

// Import all Vuetify components and directives
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Import the icons configuration from Vuetify
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// Create the Vuetify instance with components, directives, and icons configuration
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi', // Set the default icon set
    aliases, // Import aliases for the MDI icons
    sets: {
      mdi, // Specify the icon set to use
    },
  },
})

// Create and mount the Vue app with Vuetify
createApp(App).use(vuetify).mount('#app')
