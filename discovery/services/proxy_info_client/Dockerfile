FROM mhart/alpine-node

WORKDIR /app

COPY app /app

RUN npm install

EXPOSE 3000

CMD ["node", "src/app.js"]