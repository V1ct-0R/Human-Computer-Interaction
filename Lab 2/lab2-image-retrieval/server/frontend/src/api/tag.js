import request from "@/utils/request";

export function getTags() {
  return request({
    url: "/api/tags",
    method: "get"
  });
}
