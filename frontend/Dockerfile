FROM node:18 AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8080"]