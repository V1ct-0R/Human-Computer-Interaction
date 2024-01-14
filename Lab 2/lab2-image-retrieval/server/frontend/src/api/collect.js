import request from "@/utils/request";

export function collectImageById(id) {
  return request({
    url: "/api/collect",
    method: "get",
    params: { id: id }
  });
}

export function getAllCollection() {
  return request({
    url: "/api/collection",
    method: "get"
  });
}
