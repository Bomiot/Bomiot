import { defineStore } from 'pinia'


export const useExpireStore = defineStore('expire', {
  state: () => ({
    expire: 1949973210
  }),

  getters: {
    expireDataGet (state) {
      return state.expire
    },
    expireDayGet (state) {
      const now = Math.floor(Date.now() / 1000)
      var expire_sec = Math.ceil((state.expire - now) / 86400)
      return expire_sec
    }
  },

  actions: {
    expireChange (e) {
      this.expire = e
    }
  },
  persist: {
    enable: true
  }
})
