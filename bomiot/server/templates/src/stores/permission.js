import { defineStore } from 'pinia'

export const usePermissionStore = defineStore('permission', {
  state: () => ({
    permission: []
  }),

  getters: {
    permissionGet (state) {
      return state.permission
    }
  },

  actions: {
    permissionChange (e) {
      this.permission = e
    }
  },
  persist: {
    enable: true
  }
})
