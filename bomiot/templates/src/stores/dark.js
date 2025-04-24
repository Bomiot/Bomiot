import { defineStore } from 'pinia'
import { Dark } from 'quasar'

export const useDarkStore = defineStore('dark', {
  state: () => ({
    darkMode: false
  }),

  getters: {
    darkModeDataGet (state) {
      return state.darkMode
    }
  },

  actions: {
    darkModeChange () {
      Dark.toggle()
      this.darkMode = Dark.isActive
    }
  },
  persist: {
    enable: true
  }
})
