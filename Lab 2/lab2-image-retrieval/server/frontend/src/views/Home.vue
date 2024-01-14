<template>
  <div class="home">
    <el-row>
      <el-col :span="8">
        <div style="text-align: center">
          <div class="text">欢迎使用图像搜索工具</div>
        </div>
      </el-col>
      <el-col :span="16">
        <div style="margin-top: 5%;">
          <UploadImage
            v-bind:fileList="fileList"
            ref="uploadImage"
            @uploadSuccess="uploadSuccess"
          />
          <el-button
            :icon="isSearching ? 'el-icon-loading' : 'el-icon-search'"
            :disabled="fileList.length == 0 || isSearching"
            @click="searchRes"
            type="primary"
            style="margin-top: 2%; z-index: 1000;"
            circle
          ></el-button>
        </div>
      </el-col>
    </el-row>

    <el-divider></el-divider>

    <div v-if="responseImage.length != 0">
      <el-row>
        <el-col :span="16">
          <div style="width: 90%;margin:0 auto" class="containerFlex">
            <div v-for="(item, index) in responseImage" :key="index">
              <ImageCard
                :imageUrl="item"
                :disallowedTags="disallowedTags"
                :hideTags="true"
                :imageId="item"
              />
            </div>
          </div>
        </el-col>
        <el-col :span="3">
          <el-divider direction="vertical"></el-divider>
        </el-col>
        <el-col :span="5">
          <!--tag列表-->
          <div class="label-list">
            <div v-for="(item, index) in tags" :key="index">
              <el-tag :type="labelColor[index % labelColor.length]" :hit="true">
                <el-checkbox v-model="item.status" @change="tagChange" />
                {{ item.name }}({{ item.size }})
              </el-tag>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <el-empty description="暂无结果"></el-empty>
    </div>

    <el-divider></el-divider>

    <el-button
      type="primary"
      plain
      icon="el-icon-star-off"
      class="favorite-button"
      @click="openCollection"
      @changeCollect="getCollection"
      :disabled="collectDialogVisible"
    >
      查看我的收藏
    </el-button>

    <!--收藏界面-->
    <el-dialog
      title="Collection"
      :visible.sync="collectDialogVisible"
      :close-on-click-modal="false"
      :modal-append-to-body="false"
      width="65%"
    >
      <div v-loading="isCollectionLoading">
        <div
          style="margin:0 auto"
          class="containerFlex"
          v-if="collectImage.length != 0"
        >
          <div
            v-for="(item, index) in collectImage.slice(
              (currentPage - 1) * 3,
              currentPage * 3
            )"
            :key="index"
          >
            <ImageCard
              :imageUrl="item"
              :disallowedTags="disallowedTags"
              :hideTags="false"
              :imageId="item"
            />
          </div>
          <!--分页符-->
        </div>
        <div v-else>
          <el-empty description="暂无收藏"></el-empty>
        </div>
      </div>
      <el-pagination
        background
        layout="prev, pager, next"
        :hide-on-single-page="true"
        :page-size="3"
        @current-change="handleCurrentChange"
        :total="collectImage.length"
      >
      </el-pagination>
    </el-dialog>
  </div>
</template>

<script>
import UploadImage from "@/components/UploadImage.vue";
import ImageCard from "@/components/ImageCard.vue";
import { getTags } from "@/api/tag";
import { getAllCollection } from "@/api/collect";

export default {
  name: "Home",

  components: {
    UploadImage,
    ImageCard
  },

  data() {
    return {
      labelColor: ["", "success", "info", "warning", "danger"],
      fileList: [],
      responseImage: [],
      filterImage: [],
      tags: [],
      disallowedTags: [],
      collectImage: [],
      collectDialogVisible: false,
      currentPage: 1,
      isSearching: false,
      isCollectionLoading: false,
      imageUrl: ""
    };
  },

  created() {
    getTags()
      .then(response => {
        console.log(response);
        this.tags = response.map(item => {
          item.status = true;
          return item;
        });
        this.disallowedTags = [];
      })
      .catch(error => {
        console.log(error);
      });
  },

  methods: {
    uploadSuccess(response) {
      console.log("father", response);
      this.responseImage = response;
      this.isSearching = false;
    },
    searchRes() {
      this.isSearching = true;
      this.$refs.uploadImage.submitUpload();
    },
    tagChange() {
      let disallowedTags = [];
      this.tags.forEach(item => {
        if (!item.status) {
          disallowedTags.push(item.name);
        }
      });
      this.disallowedTags = disallowedTags;
    },
    openCollection() {
      this.getCollection();
      this.collectDialogVisible = true;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    getCollection() {
      this.isCollectionLoading = true;
      getAllCollection()
        .then(response => {
          console.log(response);
          this.collectImage = response;
          console.log(this.collectImage);
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          this.isCollectionLoading = false;
        });
    }
  }
};
</script>

<style scoped>
.containerFlex {
  display: flex;
  flex-direction: row;
  /*容器内成员的排列方式为从左到右*/
  flex-wrap: wrap;
  /*换行方式，放不下就换行*/
  justify-content: flex-start;
  /*项目在主轴上的对齐方式*/
  align-content: flex-start;
}
.el-divider--vertical {
  height: 60em !important;
  width: 1.5px !important;
}
.el-tag {
  float: left;
  white-space: nowrap;
  word-break: break-all;
  margin-top: 5px;
  margin-left: 5px;
}
.favorite-button {
  position: fixed;
  bottom: 5%;
  right: 5%;
  z-index: 999999;
  border-radius: 20px;
}
.text {
  font-size: 30px;
  text-align: center;
  height: 30px;
  line-height: 30px;
  margin-left: 200px;
  margin-right: 0px;
  margin-top: 75px;
  margin-bottom: 75px;
}
</style>
