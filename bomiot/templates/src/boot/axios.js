import { boot } from 'quasar/wrappers';
import axios from 'axios';
import emitter from './bus';
import { LocalStorage, Notify, Loading } from 'quasar';

const api = axios.create({
  // baseURL: 'http://127.0.0.1:8008', // Replace with your actual API URL
  withCredentials: true, // This allows cookies to be sent with requests
  headers: {
    'Referrer-Policy': 'origin-when-cross-origin'
  }
})

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
    emitter.emit('expire', parseInt(response.headers.expire))
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

function get({ url, params }) {
  return api.get(url, {
    params: { ...params },
  });
}

function post (url, data) {
  return api.post(url, data);
}

function put (url, data) {
  return api.put(url, data);
}

function patch (url, data) {
  return api.patch(url, data);
}

function deleteData (url) {
  return api.delete(url);
}


export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
})

export { api, get, post, put, patch, deleteData };
