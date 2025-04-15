import { defineStore } from 'pinia'


export const useMenuDataStore = defineStore('menu', {
  state: () => ({
    menuData: { tab: 'test1', title: '', icon: 'home', link: '/', routerTo: '/' },
    homeData: { tab: 'test1', title: '', icon: 'home', link: '/', routerTo: '/' },
  }),

  getters: {
    menuDataGet (state) {
      return state.menuData
    },
    homePageGet (state) {
      return state.homeData
    },
  },

  actions: {
    menuDataChange (e) {
      this.menuData = e
    },
    homePage (e) {
      this.homeData = e
    }
  },
})
