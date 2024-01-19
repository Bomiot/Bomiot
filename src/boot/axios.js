import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { LocalStorage, Notify } from 'quasar'
import { i18n } from './i18n'


const api = axios.create({
  baseURL: 'http://127.0.0.1:8008',
})

let lang = 'en'
if (LocalStorage.has('language')) {
  var langCheck = JSON.parse(LocalStorage.getItem('language'))
  for (const key in langCheck) {
    if (key === 'langData') {
      const value = langCheck[key]
      lang = value
    }
  }
}

api.interceptors.request.use(
  function (config) {
    config.headers.post['Content-Type'] = 'application/json, charset="utf-8"'
    config.headers.language = lang
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  function (response) {
    if (response.data.detail) {
      if (response.data.detail !== 'success') {
        Notify.create({
          message: response.data.detail,
          icon: 'close',
          color: 'negative',
          timeout: 1500
        })
      }
    }
    return response.data
  },
  function (error) {
    const defaultNotify = {
      message: i18n.t('notice.network_error'),
      icon: 'close',
      color: 'negative',
      timeout: 1500
    }
    if (error.code === 'ECONNABORTED' || error.message.indexOf('timeout') !== -1 || error.message === 'Network Error') {
      defaultNotify.message = i18n.t('notice.network_error')
      Notify.create(defaultNotify)
      return Promise.reject(error)
    }
    switch (error.response.status) {
      case 400:
        defaultNotify.message = i18n.t('notice.400')
        Notify.create(defaultNotify)
        break
      case 401:
        defaultNotify.message = i18n.t('notice.401')
        Notify.create(defaultNotify)
        break
      case 403:
        defaultNotify.message = i18n.t('notice.403')
        Notify.create(defaultNotify)
        break
      case 404:
        defaultNotify.message = i18n.t('notice.404')
        Notify.create(defaultNotify)
        break
      case 405:
        defaultNotify.message = i18n.t('notice.405')
        Notify.create(defaultNotify)
        break
      case 408:
        defaultNotify.message = i18n.t('notice.408')
        Notify.create(defaultNotify)
        break
      case 409:
        defaultNotify.message = i18n.t('notice.409')
        Notify.create(defaultNotify)
        break
      case 410:
        defaultNotify.message = i18n.t('notice.410')
        Notify.create(defaultNotify)
        break
      case 500:
        defaultNotify.message = i18n.t('notice.500')
        Notify.create(defaultNotify)
        break
      case 501:
        defaultNotify.message = i18n.t('notice.501')
        Notify.create(defaultNotify)
        break
      case 502:
        defaultNotify.message = i18n.t('notice.502')
        Notify.create(defaultNotify)
        break
      case 503:
        defaultNotify.message = i18n.t('notice.503')
        Notify.create(defaultNotify)
        break
      case 504:
        defaultNotify.message = i18n.t('notice.504')
        Notify.create(defaultNotify)
        break
      case 505:
        defaultNotify.message = i18n.t('notice.505')
        Notify.create(defaultNotify)
        break
      default:
        Notify.create(defaultNotify)
        break
    }
    return Promise.reject(error)
  }
)


export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { api }
