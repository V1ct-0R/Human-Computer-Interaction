<template>
  <div>
    <el-upload
      action="#"
      :class="uploadDisabled"
      :limit="1"
      list-type="picture-card"
      :multiple="false"
      :file-list="fileList"
      :on-success="uploadSuccess"
      :on-change="handleChange"
      :http-request="upload"
      accept="image/png, image/jpeg"
    >
      <i slot="default" class="el-icon-plus"></i>
      <div slot="file" slot-scope="{ file }">
        <img :src="file.url" alt="" class="el-upload-list__item-thumbnail" />
        <span class="el-upload-list__item-actions">
          <span
            class="el-upload-list__item-preview"
            @click="handlePictureCardPreview(file)"
          >
            <i class="el-icon-zoom-in"></i>
          </span>
          <span
            v-if="!disabled"
            class="el-upload-list__item-delete"
            @click="handleRemove(file)"
          >
            <i class="el-icon-delete"></i>
          </span>
        </span>
      </div>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible">
      <img width="80%" height="80%" :src="dialogImageUrl" alt="" />
    </el-dialog>
  </div>
</template>

<script>
import { uploadImage } from "@/api/image";
import { postTest } from "@/api/test";

export default {
  name: "UploadImage",

  data() {
    return {
      dialogImageUrl: "",
      dialogVisible: false,
      disabled: false,
      uploadDisabled: "",
      img: ""
    };
  },

  props: {
    fileList: Array
  },

  methods: {
    handleRemove(file) {
      this.fileList.splice(0, 1);
      this.uploadDisabled = "";
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    uploadSuccess(response) {
      this.$emit("uploadSuccess", response);
      console.log("uploadSuccess", response);
    },
    handleChange(file) {
      if (this.fileList.length == 1) {
        return;
      }
      this.fileList.push(file);
      if (this.fileList.length > 0) {
        this.uploadDisabled = "disabled";
      }
    },
    upload(file) {
      const formData = new FormData();
      formData.append("file", file.raw);
      postTest(formData)
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    },
    submitUpload() {
      var that = this;
      const formData = new FormData();
      formData.append("file", that.fileList[0].raw);
      uploadImage(formData)
        .then(response => {
          console.log(response);
          this.$emit("uploadSuccess", response);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style>
.disabled .el-upload--picture-card {
  display: none;
}
</style>
