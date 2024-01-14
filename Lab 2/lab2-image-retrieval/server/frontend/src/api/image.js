import request from "@/utils/request";

export function getImageById(id) {
  return request({
    url: "/api/image",
    method: "get",
    params: { id: id },
    responsetype: "blob"
  });
}

export function getImageInfoById(id) {
  return request({
    url: "/api/imageInfo",
    method: "get",
    params: { id: id }
  });
}

export function uploadImage(data) {
  return request({
    url: "/api/imageUpload",
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data"
    },
    data
  });
}
