import { defineStore } from 'pinia'


export const useLanguageStore = defineStore('language', {
  state: () => ({
    langData: 'en-US',
    langOptionsData: [
      { value: 'en-US', label: 'English' },
      { value: 'zh-CN', label: '中文简体' }
    ],
  }),

  getters: {
    langGet (state) {
      return state.langData
    },
    langOptionGet (state) {
      return state.langOptionsData
    },
  },

  actions: {
    LangChange: function (e) {
      this.langData = e
    },
    langOptionsChange (e) {
      this.lanOptionsData = e
    }
  },
  persist: {
    enable: true
  }
})
