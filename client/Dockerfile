FROM node:22-alpine
RUN corepack enable pnpm
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install
COPY . .
# Port 3000 for the Dashboard
CMD ["pnpm", "dev"]