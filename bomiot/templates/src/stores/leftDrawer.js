import { defineStore } from 'pinia'


export const useleftDrawerStore = defineStore('leftDrawer', {
  state: () => ({
    leftDrawerMenu: false,
    leftDrawerOpen: true,
  }),

  getters: {
    leftDrawerMenuGet(state) {
      return state.leftDrawerMenu
    },
    leftDrawerOpenGet(state) {
      return state.leftDrawerOpen
    },
  },

  actions: {
    controlleftDrawer (e) {
      this.leftDrawerOpen = e
    },
    toggleleftDrawer() {
      if (this.leftDrawerOpen === false) {
        this.leftDrawerOpen = true
      } else {
        this.leftDrawerOpen = false
      }
    },
    controlleftDrawerMenu (e) {
      this.leftDrawerMenu = e
    },
  },
  persist: {
    enable: true
  }
})
