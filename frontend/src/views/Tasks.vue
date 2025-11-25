<template>
  <div>
    <TasksHeader />

    <h1>Мои задачи</h1>

    <form @submit.prevent="createTask">
      <input v-model="newTask.title" placeholder="Название задачи" required />
      <textarea v-model="newTask.description" placeholder="Описание (необязательно)"></textarea> 
      <button type="submit">Создать</button>
    </form>

    <ul>
      <li v-for="task in tasks" :key="task.id">

        <span :style="{ textDecoration: task.completed ? 'line-through' : 'none' }">
          <strong>{{ task.title }}</strong><br/>
          <p v-if="task.description">{{ task.description }}</p>
        </span>

        <input
          type="checkbox"
          :checked="task.completed"
          @change="toggleDone(task)"
        />

        <button @click="deleteTask(task.id)" style="margin-left: 10px; color: red;">
          ✖
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import TasksHeader from "./TasksHeader.vue";

export default {
  name: "TasksPage",
  components: { TasksHeader },
  data() {
    return {
      tasks: [],
      newTask: {
        title: "",
        description: ""
      }
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
          headers: { Authorization: `Bearer ${token}` }
        });
        this.tasks = res.data;
      } catch {
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
        await this.getTasks();
      } catch {
        alert("Не удалось создать задачу");
      }
    },

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
        task.completed = res.data.completed;
      } catch {
        alert("Ошибка при обновлении задачи");
      }
    },

    
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

<style scoped>
form {
  margin: 15px 0;
}

input, textarea {
  display: block;
  width: 100%;
  margin-bottom: 8px;
  padding: 6px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

ul {
  list-style-type: none;
  padding-left: 0;
}
</style>