import { defineStore } from 'pinia'


export const userightDrawerStore = defineStore('rightDrawer', {
  state: () => ({
    rightDrawerMenu: false,
    rightDrawerOpen: false,
  }),

  getters: {
    rightDrawerMenuGet(state) {
      return state.rightDrawerMenu
    },
    rightDrawerOpenGet(state) {
      return state.rightDrawerOpen
    },
  },

  actions: {
    controlRightDrawer (e) {
      this.rightDrawerOpen = e
    },
    toggleRightDrawer() {
      if (this.rightDrawerOpen === false) {
        this.rightDrawerOpen = true
      } else {
        this.rightDrawerOpen = false
      }
    },
    controlRightDrawerMenu (e) {
      this.rightDrawerMenu = e
    },
  },
  persist: {
    enable: true
  }
})
