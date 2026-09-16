import { defineStore } from 'pinia'


export const useTabDataStore = defineStore('tab', {
  state: () => ({
    tabData: 'guide'
  }),

  getters: {
    tabDataGet (state) {
      return state.tabData
    }
  },

  actions: {
    tabDataChange (e) {
      this.tabData = e
    }
  },
  persist: {
    enable: true
  }
})
