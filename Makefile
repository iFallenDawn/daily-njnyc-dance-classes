SHELL := /bin/bash

BUILD_DIR := docker
ENV_DIR := $(BUILD_DIR)/env

# static env variables
include $(ENV_DIR)/static.env
-include $(ENV_DIR)/user.env

all: $(ENV_DIR)/user.env

# env variable management
$(ENV_DIR)/user.env: 
	@if [ ! -f $(ENV_DIR)/user.env ]; then \
		echo -e "\033[33m⚙️  [INFO]\033[0m user.env file not found. Creating now ..."; \
		bash $(ENV_DIR)/generate_user_env.sh $(ENV_DIR); \
		echo -e "\033[32m✅ [INFO]\033[0m user.env file created. Please update it with your configurations."; \
	fi
	
## docker
up:
	@echo -e "\033[32m🚀 [INFO]\033[0m Starting App..."
	@cd docker && docker compose --env-file env/static.env --env-file env/user.env up -d
	@echo -e "\033[32m✅ [INFO]\033[0m App is up and running! 🚀"
	@echo -e "\033[32m🌐 [INFO]\033[0m frontend: http://localhost:$(FRONTEND_PORT)"
	@echo -e "\033[32m🌐 [INFO]\033[0m backend: http://localhost:$(BACKEND_PORT)/docs"
	@echo -e "\033[32m🌐 [INFO]\033[0m documentation: http://localhost:9999"
	
down:
	@echo -e "\033[33m⏹️  [INFO]\033[0m Stopping App..."
	@cd docker && docker compose down
	@echo -e "\033[31m🛑 [INFO]\033[0m App stopped."

restart-all:
	@echo -e "\033[34m🔄 [INFO]\033[0m Restarting all containers..."
	@cd docker && docker compose restart
	@echo -e "\033[34m✅ [INFO]\033[0m All containers restarted."

restart-frontend:
	@echo -e "\033[34m🔄 [INFO]\033[0m Restarting frontend container..."
	@cd docker && docker compose restart frontend
	@echo -e "\033[34m✅ [INFO]\033[0m Frontend container restarted."

restart-backend:
	@echo -e "\033[34m🔄 [INFO]\033[0m Restarting backend container..."
	@cd docker && docker compose restart backend
	@echo -e "\033[34m✅ [INFO]\033[0m Backend container restarted."

# Generic rebuild with container parameter
rebuild:
	@if [ -z "$(service)" ]; then \
			echo -e "\033[31m❌ [ERROR]\033[0m Please specify a service: make rebuild service=<service_name>"; \
			echo -e "\033[33m💡 [HINT]\033[0m Available services: frontend, backend"; \
			exit 1; \
	fi
	@echo -e "\033[34m🔨 [INFO]\033[0m Rebuilding $(service) container...\033[0m"
	@cd docker && docker compose build $(service)

# Generic rebuild with no cache and container parameter
rebuild-no-cache:
	@if [ -z "$(service)" ]; then \
			echo -e "\033[31m❌ [ERROR]\033[0m Please specify a service: make rebuild-no-cache service=<service_name>"; \
			echo -e "\033[33m💡 [HINT]\033[0m Available services: frontend, backend"; \
			exit 1; \
	fi
	@echo -e "\033[35m🔄 [INFO]\033[0m Rebuilding $(service) container (no cache)...\033[0m"
	@cd docker && docker compose build --no-cache $(service)
	
## local development
frontend:
	cd frontend && npm i && npm run dev

backend:
	cd backend && uvicorn main:app --reload
