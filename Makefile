# ----------------------------
# Cross-platform Makefile (Windows + macOS/Linux)
# Targets: help, install
# ----------------------------

PROJECT_NAME ?= chatbot
COMPOSE_FILE ?= docker-compose.yml

# ---------- Cross-platform settings ----------
ifeq ($(OS),Windows_NT)
  SHELL := cmd.exe
  .SHELLFLAGS := /c
  DC ?= docker compose

  CHECK_DOCKER   := where docker >nul 2>nul
  CHECK_COMPOSE  := (docker compose version >nul 2>nul) || (where docker-compose >nul 2>nul)

  PRINT_OK      = echo Tools detected: docker and $(DC)
  PRINT_MISSING = $(MAKE) _print-missing-win && exit 2
else
  SHELL := /bin/sh
  DC := $(shell if command -v docker >/dev/null 2>&1; then \
              if docker compose version >/dev/null 2>&1; then echo "docker compose"; \
              elif command -v docker-compose >/dev/null 2>&1; then echo "docker-compose"; \
              else echo ""; fi; \
            else echo ""; fi)

  CHECK_DOCKER   := command -v docker >/dev/null 2>&1
  CHECK_COMPOSE  := (docker compose version >/dev/null 2>&1) || command -v docker-compose >/dev/null 2>&1

  PRINT_OK      = @echo "Tools detected: docker and $(DC)"
  PRINT_MISSING = @$(MAKE) _print-missing-unix; exit 2
endif

.PHONY: help install check-tools _print-missing-win _print-missing-unix

# ---------- help ----------
help:
	@echo Available commands:
	@echo make                Show this help
	@echo make install        Build images and install Python deps inside the app container
	@echo make run            Run the service and all related services
	@echo make down           Stop the service and all related services
	@echo make clean          Remove containers
	@echo make test           Run tests


# ---------- tool checks (cross-platform) ----------
check-tools:
	@setlocal & $(CHECK_DOCKER) && $(CHECK_COMPOSE) && ( $(PRINT_OK) ) || ( $(PRINT_MISSING) )

# ---------- install ----------
install: check-tools
	@echo "==> Building images..."
	@$(DC) -f $(COMPOSE_FILE) --project-name $(PROJECT_NAME) build
	@echo "Installation completed."

# ---------- run ----------
run:
	@echo "==> Running service"
	@$(DC) -f $(COMPOSE_FILE) --project-name $(PROJECT_NAME) up


# ---------- down ----------
down:
	@echo "==> Stopping service"
	@$(DC) -f $(COMPOSE_FILE) --project-name $(PROJECT_NAME) down

# ---------- clean ----------
clean: check-tools
	@echo "==> Removing containers, volumes, and local images for project '$(PROJECT_NAME)'..."
ifeq ($(OS),Windows_NT)
	@$(DC) -f $(COMPOSE_FILE) --project-name $(PROJECT_NAME) down -v --remove-orphans --rmi local || exit 0
else
	@$(DC) -f $(COMPOSE_FILE) --project-name $(PROJECT_NAME) down -v --remove-orphans --rmi local || true
endif
	@echo "✅ Cleanup completed."


# ---------- missing tool hints ----------
_print-missing-win:
	@echo.
	@echo "Required tools not found."
	@echo "Install Docker Desktop (includes docker + docker compose) from:"
	@echo "  https://docs.docker.com/desktop/"
	@echo "If you need GNU Make on Windows: Chocolatey ->  choco install make  (admin PowerShell)"
	@echo "Or Scoop (no admin) ->  scoop install make"
	@echo.

_print-missing-unix:
	@echo ""
	@echo "Required tools not found."
	@echo "Install Docker: https://docs.docker.com/get-started/"
	@echo "Ensure either 'docker compose' (preferred) or 'docker-compose' is available."
	@echo "Install GNU Make via your package manager (e.g., 'xcode-select --install' on macOS, 'apt install make' on Debian/Ubuntu)."
	@echo ""
