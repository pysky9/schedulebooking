<template>
  <div class="calendar-view">
    <h1>預約行事曆</h1>
    <BookedCalendar />
  </div>
</template>

<script>
import BookedCalendar from '../components/BookedCalendar.vue'

export default {
  name: 'CalendarView',
  components: {
    BookedCalendar
  }
}
</script>

<style scoped>
.calendar-view {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: var(--primary-color);
}
</style>
