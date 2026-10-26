import { defineStore } from 'pinia'


export const useMDDataStore = defineStore('markdownDocs', {
  state: () => ({
    mdDocs: "'# Hi!! Bomiot'",
    docName: ''
  }),

  getters: {
    mdDocsGet (state) {
      return state.mdDocs
    },
    docNameGet (state) {
      return state.docName
    },
  },

  actions: {
    mdDocsChange(e) {
      this.mdDocs = e
    },
    docNameChange(e) {
      this.docName = e
    },
  }
})
