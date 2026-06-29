FROM node:20-alpine

WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm ci

# Copy application code
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
