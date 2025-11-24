<template>
  <div>
    <h1>Мои задачи</h1>

    <form @submit.prevent="createTask">
      <input v-model="newTask.title" placeholder="Название задачи" required />
      <input v-model="newDescription.description" placeholder="Описание (необязательно)" />
      <button type="submit">Создать</button>
    </form>

    <ul>
      <li v-for="task in tasks" :key="task.id">

        <!-- Текст задачи -->
        <span :style="{ textDecoration: task.completed ? 'line-through' : 'none' }">
          <strong>{{ task.title }}</strong>
          <p v-if="task.description">{{ task.description }}</p>
        </span>

        <!-- Галочка -->
        <input
          type="checkbox"
          :checked="task.completed"
          @change="toggleDone(task)"
        />

        <!-- Крестик удалить -->
        <button @click="deleteTask(task.id)" style="margin-left: 10px; color: red;">
          ✖
        </button>
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
      newTask: "",
      newDescription: ""
    };
  },
  async mounted() {
    await this.getTasks();
  },
  methods: {
    // Получить задачи
    async getTasks() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://127.0.0.1:8000/tasks", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.tasks = res.data;
      } catch {
        alert("Не удалось загрузить задачи");
      }
    },

    // Создать задачу
    async createTask() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.post(
          "http://127.0.0.1:8000/tasks",
          { title: this.newTask, description: this.newDescription },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.tasks.push(res.data);
        this.newTask = "";
        this.newDescription = "";
      } catch {
        alert("Не удалось создать задачу");
      }
    },

    // Отметить как выполненную
    async toggleDone(task) {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.put(
          `http://127.0.0.1:8000/tasks/${task.id}`,
          {
            completed: !task.completed,
            title: task.title,
            description: task.description
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        task.is_done = res.data.is_done;
      } catch {
        alert("Ошибка при обновлении задачи");
      }
    },

    // Удалить задачу
    async deleteTask(id) {
      if (!confirm("Удалить задачу?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.delete(`http://127.0.0.1:8000/tasks/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.tasks = this.tasks.filter(t => t.id !== id);
      } catch {
        alert("Не удалось удалить задачу");
      }
    }
  }
};
</script>