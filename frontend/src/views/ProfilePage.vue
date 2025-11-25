<template>
  <div class="profile-container">
    <h1>Профиль</h1>

    <form @submit.prevent="updateProfile" class="profile-form">
      <label>Никнейм:</label>
      <input v-model="user.username" required />

      <label>Email:</label>
      <input v-model="user.email" type="email" required />

      <label>Имя:</label>
      <input v-model="user.first_name" />

      <label>Фамилия:</label>
      <input v-model="user.last_name" />

      <label>Новый пароль (необязательно):</label>
      <input v-model="user.password" type="password" />

      <button type="submit">Сохранить изменения</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfilePage",
  data() {
    return {
      user: {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password: ""
      }
    };
  },
  async mounted() {
    await this.loadProfile();
  },
  methods: {
    async loadProfile() {
      const token = localStorage.getItem("token");

      const res = await axios.get("http://127.0.0.1:8000/profile", {
        headers: { Authorization: `Bearer ${token}` }
      });

      this.user = {
        username: res.data.username,
        email: res.data.email,
        first_name: res.data.first_name,
        last_name: res.data.last_name,
        password: ""
      };
    },

    async updateProfile() {
      const token = localStorage.getItem("token");

      await axios.put(
        "http://127.0.0.1:8000/profile/update",
        this.user,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      alert("Профиль обновлён");
      this.user.password = ""; // очистка поля после сохранения
    }
  }
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 90vh; /* Центрируем по вертикали */
  background-color: #f7f9fc;
  padding: 20px;
}

.profile-container h1 {
  margin-bottom: 20px;
  color: #333;
}

.profile-form {
  background-color: #ffffff;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  display: flex;
  flex-direction: column;
}

.profile-form label {
  margin-top: 10px;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.profile-form input {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.profile-form button {
  margin-top: 20px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #3498db;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.profile-form button:hover {
  background-color: #2c80c3;
}
</style>