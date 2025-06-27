import { boot } from 'quasar/wrappers';
import axios from 'axios';
import emitter from './bus';
import { LocalStorage, Notify, Loading } from 'quasar';

const baseURL = 'http://127.0.0.1:8000' // Replace with your actual API URL

const api = axios.create({
  // baseURL: baseURL
})

class RequestThrottler {
  constructor(interval = 250) {
    this.interval = interval
    this.lastRequestTime = 0
    this.pendingRequests = []
    this.isProcessing = false
  }

  async throttleRequest(requestFn) {
    return new Promise((resolve, reject) => {
      this.pendingRequests.push({ requestFn, resolve, reject })
      this.processQueue()
    })
  }

  async processQueue() {
    if (this.isProcessing || this.pendingRequests.length === 0) {
      return
    }
    this.isProcessing = true
    while (this.pendingRequests.length > 0) {
      const now = Date.now();
      const timeSinceLastRequest = now - this.lastRequestTime;
      if (timeSinceLastRequest < this.interval) {
        await this.delay(this.interval - timeSinceLastRequest);
      }
      const { requestFn, resolve, reject } = this.pendingRequests.shift();
      this.lastRequestTime = Date.now();
      try {
        const result = await requestFn();
        resolve(result);
      } catch (error) {
        reject(error);
      }
    }
    this.isProcessing = false;
  }
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

const requestThrottler = new RequestThrottler(250)

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

async function throttledGet({ url, params }) {
  return requestThrottler.throttleRequest(() => 
    api.get(url, { params: { ...params } })
  );
}

async function throttledPost(url, data) {
  return requestThrottler.throttleRequest(() => 
    api.post(url, data)
  );
}

async function throttledPut(url, data) {
  return requestThrottler.throttleRequest(() => 
    api.put(url, data)
  );
}

async function throttledPatch(url, data) {
  return requestThrottler.throttleRequest(() => 
    api.patch(url, data)
  );
}

async function throttledDelete(url) {
  return requestThrottler.throttleRequest(() => 
    api.delete(url)
  );
}

async function throttledFileUpload(url, formData, onProgress = null) {
  return requestThrottler.throttleRequest(() => 
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
  throttledGet as get, 
  throttledPost as post, 
  throttledPut as put, 
  throttledPatch as patch, 
  throttledDelete as deleteData,
  throttledFileUpload as fileUpload,
  baseURL
}