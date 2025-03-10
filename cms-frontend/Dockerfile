# Etapa de construcción
FROM node:18-alpine AS build

WORKDIR /app

COPY cms-frontend/package.json cms-frontend/package-lock.json ./
RUN npm install --production

COPY cms-frontend ./
RUN npm run build

# Etapa de producción
FROM nginx:stable-alpine

# Copia los archivos construidos al contenedor de nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]