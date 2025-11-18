<template>
  <div>
    <h1>Вход</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Имя пользователя" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <button type="submit">Войти</button>
    </form>

    <p>
      Нет аккаунта?
      <router-link to="/register">Зарегистрироваться</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    async login() {
      try {
        const res = await axios.post("http://127.0.0.1:8000/auth/login", {
          username: this.username,
          password: this.password
        });
        localStorage.setItem("token", res.data.access_token);
        alert("Успешный вход!");
      } catch (err) {
        alert("Ошибка входа");
      }
    }
  }
};
</script>