import request from "@/utils/request";

export function getTest() {
  return request({
    url: "/api/test",
    method: "get"
  });
}

export function postTest(data) {
  return request({
    url: "/api/test/post",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
}
