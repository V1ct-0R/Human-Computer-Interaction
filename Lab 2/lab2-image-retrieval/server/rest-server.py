# !flask/bin/python
################################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
# -------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
import base64
from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    render_template,
    Response,
    make_response,
)
from flask_cors import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from search import recommend
from tensorflow.python.platform import gfile

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

# 将flask与vue前端连接起来
app = Flask(
    __name__,
    template_folder="./frontend/dist",
    static_folder="./frontend/dist",
    static_url_path="",
)
# 解决跨域问题
CORS(app, supports_credentials=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# ==============================================================================================================================
#
#    Loading the extracted feature vectors for image retrieval
#
#
# ==============================================================================================================================
extracted_features = np.zeros((2955, 2048), dtype=np.float32)

tag_type = [
    "animals",
    "baby",
    "bird",
    "car",
    "clouds",
    "dog",
    "female",
    "flower",
    "food",
    "indoor",
    "lake",
    "male",
    "night",
    "people",
    "plant_life",
    "portrait",
    "river",
    "sea",
    "structures",
    "sunset",
    "transport",
    "tree",
    "water",
]


# 建立映射关系
def image_tags():
    typeDict = dict()
    for i in tag_type:
        typeDict[i] = []
        # 读取对应的文件
        with open("database/tags/" + i + ".txt", "r") as fp:
            l = fp.readlines()
            for j in l:
                typeDict[i].append(j.strip())
    return typeDict


typeDict = image_tags()

with open("saved_features_recom.txt") as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
print("loaded extracted_features")


# 获取标签列表，按照标签的数量排序
@app.route("/tags", methods=["GET"])
def get_tags():
    res = []
    # 遍历所有的标签
    for i in typeDict.keys():
        res.append(
            {
                "name": i,
                "size": len(typeDict[i]),
            }
        )
    res.sort(key=lambda x: x["size"], reverse=True)
    return jsonify(res)


# 根据图片id获取图片
@app.route("/image", methods=["GET"])
def get_image():
    id = request.values.get("id")

    # 读取图片
    with open("database/dataset/im" + id + ".jpg", "rb") as f:
        image = f.read()

    response = make_response(image)
    response.headers["Content-Type"] = "image/jpeg"
    return response


# 收藏/取消收藏图片
@app.route("/collect", methods=["GET"])
def collect_image():
    id = request.values.get("id")

    # 读取收藏列表
    with open("database/collection.txt", "r") as f:
        l = f.readlines()

    temp = []
    isCollected = False
    # 遍历收藏列表
    for i in l:
        if i.strip() == id:
            isCollected = True
        else:
            temp.append(i.strip())
    # 如果图片未收藏，则收藏
    # 如果图片已经收藏，则取消收藏
    if not isCollected:
        temp.append(id)

    # 写入收藏列表
    n = len(temp)
    with open("database/collection.txt", "w") as f:
        for index, item in enumerate(temp):
            if index != n - 1:
                f.write(item + "\n")
            else:
                f.write(item)

    return jsonify({"status": True})


# 获取用户收藏的图片（id）
@app.route("/collection", methods=["GET"])
def get_collection():
    res = []
    with open("database/collection.txt", "r") as f:
        l = f.readlines()
        for i in l:
            res.append(i.strip())
    return jsonify(res)


# 根据图片id给出是否被收藏和标签信息
@app.route("/imageInfo", methods=["GET"])
def get_image_info():
    id = request.values.get("id")
    res = {
        "isCollected": False,
        "tags": [],
    }
    # 读取收藏列表
    with open("database/collection.txt", "r") as f:
        l = f.readlines()
    # 遍历收藏列表
    for i in l:
        if i.strip() == id:
            res["isCollected"] = True
            break

    # 遍历标签列表
    for i in typeDict.keys():
        if id in typeDict[i]:
            res["tags"].append(i)

    return jsonify(res)


# ==============================================================================================================================
#
#  This function is used to do the image search/image retrieval
#
# ==============================================================================================================================
@app.route("/imageUpload", methods=["GET", "POST"])
def upload_img():
    print("image upload")
    result = "static/result"
    if not gfile.Exists(result):
        os.mkdir(result)
    shutil.rmtree(result)

    if request.method == "POST" or request.method == "GET":
        print(request.method)
        # check if the post request has the file part
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)

        file = request.files["file"]
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            inputloc = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_list = recommend(inputloc, extracted_features)
            return jsonify(image_list)


# 测试前后端连接接口
@app.route("/test", methods=["GET"])
def test():
    return "test"


@app.route("/test/post", methods=["POST"])
def test_post():
    print(request.method)
    print(request.content_type)
    # print(request.form.to_dict())
    if "length" not in request.form:
        print("No length in request.form")
    if "file" not in request.form:
        print("No file part in request.form")
    else:
        file = request.form["file"]
        print(file)
    if "length" not in request.files:
        print("No length in request.files")
    if "file" not in request.files:
        print("No file part in request.files")
    else:
        file = request.files["file"]
        print(file.filename)
    return jsonify({"status": True})


# ==============================================================================================================================
#
#                                           Main function                                                        	            #
#
# ==============================================================================================================================
@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
