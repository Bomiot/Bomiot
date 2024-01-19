import { defineStore } from 'pinia'


export const useGiscusStore = defineStore('giscus', {
  state: () => ({
    repo: "",
    repoid: "",
    category: "",
    categoryid: "",
  }),

  getters: {
    repoGet (state) {
      return state.repo
    },
    repoidGet (state) {
      return state.repoid
    },
    categoryGet (state) {
      return state.category
    },
    categoryidGet (state) {
      return state.categoryid
    },
  },

  actions: {
    repoChange (e) {
      this.repo = e
    },
    repoidChange (e) {
      this.repoid = e
    },
    categoryChange (e) {
      this.category = e
    },
    categoryidChange (e) {
      this.categoryid = e
    },
  }
})
