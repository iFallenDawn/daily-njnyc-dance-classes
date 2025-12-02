# syntax=docker/dockerfile:1
FROM node:18-alpine

# Install dependencies for development
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Expose the development port
EXPOSE 3000

# Set environment to development
ENV NODE_ENV development

# Run the development server
CMD ["npm", "run", "dev"]
