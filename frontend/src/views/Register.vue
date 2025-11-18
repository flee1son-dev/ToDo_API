<template>
  <div>
    <h1>Регистрация</h1>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Имя пользователя" required />
      <input v-model="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <input v-model="first_name" placeholder="Имя (необязательно)" />
      <input v-model="last_name" placeholder="Фамилия (необязательно)" />
      <button type="submit">Зарегистрироваться</button>
    </form>
    <p>
      Уже есть аккаунт?
      <router-link to="/login">Войти</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      first_name: "",
      last_name: ""
    };
  },
  methods: {
    async register() {
      try {
        await axios.post("http://127.0.0.1:8000/auth/register", {
          username: this.username,
          password: this.password,
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name
        });
        alert("Регистрация прошла успешно!");
      } catch (err) {
        alert(err.response?.data?.detail || "Ошибка регистрации");
      }
    }
  }
};
</script>