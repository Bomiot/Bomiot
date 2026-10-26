import { defineStore } from 'pinia'


export const useProjectStore = defineStore('project', {
  state: () => ({
    project: 'greaterwms'
  }),

  getters: {
    projectDataGet (state) {
      return state.project
    }
  },

  actions: {
    projectChange (e) {
      this.project = e
    }
  },
  persist: {
    enable: true
  }
})
