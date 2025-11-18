// src/router.js
import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "./views/Login.vue";
import RegisterPage from "./views/Register.vue";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage
  },
  {
    path: "/",
    redirect: "/login" // по умолчанию редирект на логин
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;