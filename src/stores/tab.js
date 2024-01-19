import { defineStore } from 'pinia'


export const useTabDataStore = defineStore('tab', {
  state: () => ({
    tabData: 'test1'
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
