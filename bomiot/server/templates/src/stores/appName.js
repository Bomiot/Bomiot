import { defineStore } from 'pinia'


export const useAppNameStore = defineStore('appname', {
  state: () => ({
    appName: 'GreaterWMS'
  }),

  getters: {
    appModeDataGet (state) {
      return state.appName
    }
  },

  actions: {
    appModeChange (e) {
      this.appName = e
    }
  },
  persist: {
    enable: true
  }
})
