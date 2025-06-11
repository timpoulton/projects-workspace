FROM node:18-alpine AS builder
WORKDIR /app
COPY src/projekt-ai-website/package*.json ./
RUN npm install
COPY src/projekt-ai-website/ ./
RUN npm run build

FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
