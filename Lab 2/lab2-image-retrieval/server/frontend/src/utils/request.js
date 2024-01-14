import axios from "axios";
//import store from '@/store'
//import { Message } from 'element-ui'
import { Notification } from "element-ui";

const service = axios.create({
  //baseURL:'https://localhost:44359/api/',
  baseURL: process.env.API_ROOT, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 80000 // request timeout
  //async:true,
  //crossDomain:true,
});

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    var lang = localStorage.getItem("lang"); //因为项目中使用到了i18n国际化语言配置，请根据实际情况自行修改
    if (!lang) {
      lang = "zh_CN";
    }
    config.headers["Accept-Language"] = lang.replace(/_/g, "-");
    // config.headers["Content-Type"] = "application/json";
    return config;
  },
  error => {
    // do something with request error
    console.log(error); // for debug
    return Promise.reject(error);
  }
);

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data;
    console.log("真实的回复为：", response);
    return res;
  },
  error => {
    if (
      error.response.data instanceof Blob &&
      error.response.data.type.toLowerCase().indexOf("json") !== -1
    ) {
      const reader = new FileReader();
      reader.readAsText(error.response.data, "utf-8");
      reader.onload = function(e) {
        const errorMsg = JSON.parse(reader.result).message;
        Notification.error({
          title: errorMsg,
          duration: 5000
        });
      };
    } else {
      let code = 0;
      try {
        code = error.response.data.status;
      } catch (e) {
        if (error.toString().indexOf("Error: timeout") !== -1) {
          Notification.error({
            title: "网络请求超时",
            duration: 5000
          });
          return Promise.reject(error);
        }
      }

      if (!code) {
        Notification.error({
          title: "接口请求失败",
          duration: 5000
        });
      }
    }
    console.log("error"); // for debug
    return Promise.reject(error);
  }
);

export default service;
