import { boot } from 'quasar/wrappers';
import axios from 'axios';
import { LocalStorage, Notify, Loading } from 'quasar';

const api = axios.create({
  timeout: 10000,
});

let lang = 'en-US';
if (LocalStorage.has('language')) {
  const langCheck = JSON.parse(LocalStorage.getItem('language'));
  for (const key in langCheck) {
    if (key === 'langData') {
      const LangValue = langCheck[key];
      lang = LangValue;
    }
  }
}

let token = '';
if (LocalStorage.has('token')) {
  var tokenCheck = JSON.parse(LocalStorage.getItem('token'));
  for (const key in tokenCheck) {
    if (key === 'token') {
      const value = tokenCheck[key];
      token = value;
    }
  }
}

api.interceptors.request.use(
  (config) => {
    config.headers.token = token;
    config.headers.language = lang;
    Loading.show();
    return config;
  },
  function (error) {
    Loading.hide();
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  function (response) {
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
    Loading.hide();
    return response.data;
  }
);

function get (url) {
  return api.get(url);
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
