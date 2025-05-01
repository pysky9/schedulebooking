<template>
  <nav class="navbar navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" @click="$emit('redirect-home')">吉時約 Schedule Booking</a>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'LoginHeader',
  emits: ['redirect-home']
}
</script>

<style scoped>
.navbar {
  padding: 0.5rem 2rem;
}

.navbar-brand {
  font-family: "Microsoft Jhenghei";
  font-weight: bold;
  padding-top: 5px;
  font-size: 30px;
  cursor: pointer;
}

.btn-outline-primary {
  font-family: "Microsoft Jhenghei";
  font-size: 30px;
}
</style>
