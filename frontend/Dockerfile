# # Stage 1: Build Angular app
# FROM node:20 AS build

# WORKDIR /app

# COPY package*.json ./
# RUN npm install

# COPY . .
# RUN npx run build frontend --configuration production

# # Stage 2: Serve with nginx
# FROM nginx:alpine

# COPY --from=build /app/dist /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]


# Build stage
FROM node:20 AS build

WORKDIR /app

COPY . .
RUN npm install

COPY . .
RUN npx ng build --configuration production
# RUN npx ng build frontend --configuration production

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]