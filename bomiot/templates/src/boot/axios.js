import { boot } from 'quasar/wrappers';
import axios from 'axios';
import emitter from './bus';
import { LocalStorage, Notify, Loading } from 'quasar';

const baseURL = 'http://127.0.0.1:8000' // Replace with your actual API URL

const api = axios.create({
  // baseURL: baseURL
})

class SimpleThrottler {
  constructor(interval = 250) {
    this.interval = interval
    this.lastRequestTime = 0
  }

  async throttle() {
    const now = Date.now()
    const timeSinceLastRequest = now - this.lastRequestTime

    if (timeSinceLastRequest < this.interval) {
      const delay = this.interval - timeSinceLastRequest
      await new Promise(resolve => setTimeout(resolve, delay))
    }

    this.lastRequestTime = Date.now()
  }
}

const throttler = new SimpleThrottler(250)

api.interceptors.request.use(
  (config) => {
    let token = ''
    if (LocalStorage.has('token')) {
      var tokenCheck = JSON.parse(LocalStorage.getItem('token'))
      if (tokenCheck !== '') {
        for (const key in tokenCheck) {
          if (key === 'token') {
            const value = tokenCheck[key]
            token = value
          }
        }
      } else {
        if (config.url !== 'login/') {
          Notify.create({
            type: 'warning',
            message: 'Please Login First'
          })
          return Promise.reject(new Error('Please Login First'))
        }
      }
    }
    config.headers.token = token
    let lang = 'en-US'
    if (LocalStorage.has('language')) {
      const langCheck = JSON.parse(LocalStorage.getItem('language'))
      if (langCheck !== '') {
        for (const key in langCheck) {
          if (key === 'langData') {
            const LangValue = langCheck[key]
            lang = LangValue
          }
        }
      }
    }
    config.headers.language = lang
    let project = 'bomiot'
    if (LocalStorage.has('project')) {
      const projectCheck = JSON.parse(LocalStorage.getItem('project'))
      if (projectCheck !== '') {
        for (const key in projectCheck) {
          if (key === 'project') {
            const projectValue = projectCheck[key]
            project = projectValue
          }
        }
      }
    }
    config.headers.project = project
    Loading.show()
    return config
  },
  function (error) {
    Loading.hide()
    return Promise.reject(error)
  }
);

api.interceptors.response.use(
  (response) => {
    if (response.data.detail) {
      Notify.create({
        type: 'warning',
        message: response.data.detail
      })
    }
    if (response.data.msg) {
      Notify.create({
        type: 'success',
        message: response.data.msg
      })
    }
    if (response.data.login) {
      Notify.create({
        type: 'warning',
        message: response.data.login
      })
      emitter.emit('needLogin', true)
    } else {
      emitter.emit('needLogin', false)
    }
    Loading.hide();
    return response.data;
  }
);

async function throttledRequest(requestFn) {
  await throttler.throttle()
  return requestFn()
}

async function get({ url, params }) {
  return throttledRequest(() =>
    api.get(url, { params: { ...params } })
  );
}

async function post(url, data) {
  return throttledRequest(() =>
    api.post(url, data)
  );
}

async function put(url, data) {
  return throttledRequest(() =>
    api.put(url, data)
  );
}

async function patch(url, data) {
  return throttledRequest(() =>
    api.patch(url, data)
  );
}

async function deleteData(url) {
  return throttledRequest(() =>
    api.delete(url)
  );
}

async function fileUpload(url, formData, onProgress = null) {
  return throttledRequest(() =>
    api.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted)
        }
      }
    })
  )
}

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
})

export {
  api,
  get,
  post,
  put,
  patch,
  deleteData,
  fileUpload,
  baseURL
}
