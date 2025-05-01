<template>
  <div :id="id" class="section-container">
    <div :class="titleClass">
      <span v-html="title"></span>
      <template v-if="hasSubtitle">
        <br>
        <slot name="subtitle"></slot>
      </template>
    </div>
    <slot name="image"></slot>
  </div>
</template>

<script>
export default {
  name: 'SectionContainer',
  props: {
    id: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    titleClass: {
      type: String,
      required: true
    },
    hasSubtitle: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.section-container {
  padding-top: 60px;
  padding-bottom: 60px;
  display: flex;
  height: 524px;
}

.line-info, .setting-info, .changing-info, .calendar-info, .order-info {
  font-family: "Microsoft Jhenghei";
  font-weight: bold;
  padding-top: 50px;
  padding-left: 60px;
  font-size: 30px;
  flex: none;
  width: 50%;
}

@media (max-width: 768px) {
  .section-container {
    flex-direction: column;
    height: auto;
  }
  
  .line-info, .setting-info, .changing-info, .calendar-info, .order-info {
    width: 100%;
    padding-left: 20px;
    padding-right: 20px;
    text-align: center;
  }
}
</style>
