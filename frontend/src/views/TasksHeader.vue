<template>
  <header class="tasks-header" v-if="isAuth">
    <h2>Мои задачи</h2>
    
    <div class="buttons">
      <!-- Профиль -->
      <button class="profile-btn" @click="$router.push('/profile')">
        Профиль
      </button>

      <!-- Выйти -->
      <button class="logout-btn" @click="logout">
        Выйти
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: "TasksHeader",
  data() {
    return {
      isAuth: false
    };
  },
  mounted() {
    this.checkAuth();
  },
  watch: {
    // Обновляем статус авторизации при смене маршрута
    $route() {
      this.checkAuth();
    }
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem("token");
      this.isAuth = !!token;
    },
    logout() {
      localStorage.removeItem("token"); // удаляем токен
      this.isAuth = false;
      this.$router.push("/login");      // редирект на страницу входа
    }
  }
};
</script>

<style scoped>
.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: #f3f3f3;
  border-bottom: 1px solid #ccc;
}

.buttons {
  display: flex;
  gap: 10px;
}

.profile-btn,
.logout-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: white;
}

.profile-btn {
  background-color: #3498db;
}

.logout-btn {
  background-color: #e74c3c;
}
</style>