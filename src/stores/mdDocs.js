import { defineStore } from 'pinia'


export const useMDDataStore = defineStore('markdownDocs', {
  state: () => ({
    mdDocs: "'# Hi!! GreaterWMS'",
    tocRouter: ''
  }),

  getters: {
    mdDocsGet (state) {
      return state.mdDocs
    },
    tocRouterGet (state) {
      return state.tocRouter
    },
  },

  actions: {
    mdDocsChange(e) {
      this.mdDocs = e
    },
    tocRouterChange(e) {
      this.tocRouter = e
    },
  }
})
