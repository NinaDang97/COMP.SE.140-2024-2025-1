FROM node:22-alpine

WORKDIR /app

COPY service.js /app/

RUN npm install express

EXPOSE 5002

CMD ["node", "service.js"]