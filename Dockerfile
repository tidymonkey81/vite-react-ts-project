# Use an official Node runtime as a parent image
FROM node:latest

# Set the working directory in the Docker container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) for the frontend
COPY frontend/package.json frontend/package-lock.json* ./frontend/

# Install frontend dependencies
RUN cd frontend && npm install

# Install Python and pip for the backend
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy the backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip3 install -r backend/requirements.txt

# Copy the rest of your application code into the Docker container
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "run", "start", "--prefix", "frontend"]