<template>
  <div>
    <h1>Мои задачи</h1>
    <form @submit.prevent="createTask">
      <input v-model="newTask.title" placeholder="Название задачи" required />
      <textarea v-model="newTask.description" placeholder="Описание (необязательно)"></textarea>
      <button type="submit">Создать</button>
    </form>

    <ul>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong>
        <p v-if="task.description">{{ task.description }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TasksPage",
  data() {
    return {
      tasks: [],
      newTask: {
        title: "",
        description: ""
      },
    };
  },
  async mounted() {
    await this.getTasks();
  },
  methods: {
    async getTasks() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://127.0.0.1:8000/tasks", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.tasks = res.data;
      } catch (err) {
        alert("Не удалось загрузить задачи");
      }
    },
    async createTask() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.post(
          "http://127.0.0.1:8000/tasks",
          {
            title: this.newTask.title,
            description: this.newTask.description || null
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.tasks.push(res.data);
        this.newTask.title = "";
        this.newTask.description = "";
      } catch (err) {
        alert("Не удалось создать задачу");
      }
    }
  }
};
</script>