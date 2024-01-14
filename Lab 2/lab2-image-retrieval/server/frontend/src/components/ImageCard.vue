<template>
  <div>
    <div v-if="isTagAllowed" class="ImageCard">
      <el-image
        fit="fill"
        class="image"
        style="width: 100%; height: 62%;"
        :src="'http://localhost:8080/api/image?id=' + imageId"
      >
        <div slot="error" class="image-slot">
          <img fit="fill" class="image" src="@/assets/error.png" />
        </div>
      </el-image>

      <el-row style="margin-top: 10px;">
        <el-col :span="18">
          <div class="text">image{{ imageId }}</div>
        </el-col>

        <el-col :span="3">
          <el-tooltip
            class="item"
            effect="dark"
            :content="
              isCollectedLoading
                ? '等待中...'
                : isCollected
                ? '取消收藏'
                : '收藏'
            "
            placement="top-start"
          >
            <div v-if="!isCollectedLoading">
              <em
                :class="isCollected ? 'el-icon-star-on' : 'el-icon-star-off'"
                style="font-size: 20px;"
                @click="collectImage"
              ></em>
            </div>
            <div v-else>
              <em class="el-icon-loading" style="font-size: 20px"></em>
            </div>
          </el-tooltip>
        </el-col>

        <el-col :span="3">
          <el-tooltip
            class="item"
            effect="dark"
            content="查看大图"
            placement="top-start"
          >
            <em
              class="el-icon-zoom-in"
              style="font-size: 20px;"
              @click="viewBigImage"
            ></em>
          </el-tooltip>
        </el-col>
      </el-row>

      <div class="label-list">
        <el-tag
          type="primary"
          v-for="(tag, index) in showTags"
          :key="index"
          effect="dark"
          :hit="true"
        >
          {{ tag }}
        </el-tag>
      </div>

      <el-dialog :visible.sync="dialogVisible">
        <img
          width="80%"
          height="80%"
          :src="'http://localhost:8080/api/image?id=' + imageId"
          alt=""
        />
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { getImageById, getImageInfoById } from "@/api/image";
import { collectImageById } from "@/api/collect";

export default {
  name: "ImageCard",

  data() {
    return {
      imageSource: "",
      imageUrl: "",
      tags: [],
      isCollected: false,
      dialogVisible: false,
      isCollectedLoading: false
    };
  },

  props: {
    imageId: String,
    disallowedTags: Array,
    hideTags: Boolean
  },

  computed: {
    showTags() {
      if (this.tags.length != 0) {
        console.log(this.tags[0]);
        return this.tags.slice(0, 3);
      } else {
        return ["none"];
      }
    },
    isTagAllowed() {
      if (!this.hideTags) {
        return true;
      }
      for (let i = 0; i < this.tags.length; ++i) {
        if (this.disallowedTags.indexOf(this.tags[i]) != -1) {
          return false;
        }
      }
      return true;
    }
  },

  created() {
    getImageById(this.imageId)
      .then(response => {
        this.imageUrl = URL.createObjectURL(
          new Blob([response], { type: "image/jpeg" })
        );
        console.log(this.imageUrl);
      })
      .catch(error => {
        console.log(error);
      });
    getImageInfoById(this.imageId)
      .then(response => {
        console.log(response);
        this.isCollected = response.isCollected;
        this.tags = response.tags;
      })
      .catch(error => {
        console.log(error);
      });
  },

  methods: {
    collectImage() {
      this.isCollectedLoading = true;

      collectImageById(this.imageId)
        .then(() => {
          setTimeout(() => {
            this.isCollected = !this.isCollected;
            if (this.isCollected) {
              this.$message({
                message: "收藏成功！",
                type: "success"
              });
            } else {
              this.$message({
                message: "取消收藏成功！",
                type: "success"
              });
            }
            this.isCollectedLoading = false;
          }, 1000);
        })
        .catch(() => {
          this.isCollectedLoading = false;
        })
        .finally(() => {
          this.$emit("changeCollect");
        });
    },
    viewBigImage() {
      this.dialogVisible = true;
    }
  }
};
</script>

<style scoped>
.ImageCard {
  width: 270px;
  height: 290px;
  margin-bottom: 20px;
  margin-left: 25px;
}
.text {
  text-align: left;
  margin-left: 2%;
  margin-top: 5px;
  margin-right: 4%;
  margin-bottom: 0;
}
.label-list {
  padding: 1px 1px;
  margin: 1px 1px;
}
.el-tag {
  float: left;
  word-break: break-all;
  margin-top: 5px;
  margin-left: 5px;
  max-height: 4vh;
  color: white;
  white-space: normal;
  height: auto;
}
</style>
