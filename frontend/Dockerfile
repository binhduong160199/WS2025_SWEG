# Build the React app
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve the build with nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80