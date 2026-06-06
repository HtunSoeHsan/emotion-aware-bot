# Stage 1: Build the app
FROM node:20-alpine AS builder
WORKDIR /app

ARG BACKEND_URL
ARG NEXT_PUBLIC_API_URL
ENV BACKEND_URL=$BACKEND_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package.json yarn.lock* package-lock.json* ./
RUN \
  if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  else npm install; \
  fi

COPY . .
RUN \
  if [ -f yarn.lock ]; then yarn build; \
  else npm run build; \
  fi

# Stage 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ARG BACKEND_URL
ARG NEXT_PUBLIC_API_URL
ENV BACKEND_URL=$BACKEND_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

ENV NODE_ENV=production
ENV PORT=4001

COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./next.config.js

EXPOSE 4001

# Run the next start script
CMD ["npm", "run", "start"]
