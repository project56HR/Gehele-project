# Use official Node.js runtime as base image
FROM node:22-slim

# Set working directory inside the container
WORKDIR /app

# Copy package files first (for better caching)
COPY ui/package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of your app source
COPY ui/ .

# Expose port 3000 inside the container
EXPOSE 3000

# Run the app
CMD ["node", "app.js"]
