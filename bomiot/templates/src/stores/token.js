import { defineStore } from 'pinia'


export const useTokenStore = defineStore('token', {
  state: () => ({
    token: ''
  }),

  getters: {
    tokenDataGet (state) {
      if (state.token !== '') {
        let strings = state.token.split(".")
        var userinfo = JSON.parse(decodeURIComponent(escape(window.atob(strings[1].replace(/-/g, "+").replace(/_/g, "/")))));
        return userinfo
      } else {
        return state.token
      }
    }
  },

  actions: {
    tokenChange (e) {
      this.token = e
    },
    tokenCheck() {
      if (this.token !== '') {
        let strings = this.token.split(".")
        var userinfo = JSON.parse(decodeURIComponent(escape(window.atob(strings[1].replace(/-/g, "+").replace(/_/g, "/")))));
        var tokeninit = userinfo.exp - (Date.parse(new Date()) / 1000)
        if (tokeninit <= 0) {
          this.token = ''
        }
      }
    },
    userPermissionGet (e) {
      if (this.token !== '') {
        let strings = this.token.split(".")
        var userinfo = JSON.parse(decodeURIComponent(escape(window.atob(strings[1].replace(/-/g, "+").replace(/_/g, "/")))));
        return e in userinfo.permission;
      } else {
        return false
      }
    }
  },
  persist: {
    enable: true
  }
})
