import { defineStore } from 'pinia'


export const useMDDataStore = defineStore('markdownDocs', {
  state: () => ({
    mdDocs: "'# Hi!! GreaterWMS'",
    docName: '',
    tocRouter: ''
  }),

  getters: {
    mdDocsGet (state) {
      return state.mdDocs
    },
    docNameGet (state) {
      return state.docName
    },
    tocRouterGet (state) {
      return state.tocRouter
    },
  },

  actions: {
    mdDocsChange(e) {
      this.mdDocs = e
    },
    docNameChange(e) {
      this.docName = e
    },
    tocRouterChange(e) {
      this.tocRouter = e
    },
  }
})
