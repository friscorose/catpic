CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -Iinclude
LDFLAGS =

SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include

# Add your source files here
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

all: $(BUILD_DIR)
	@echo "Build targets not yet implemented"

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

test:
	@echo "Tests not yet implemented"
	@exit 1

test-vectors:
	@echo "Compliance tests not yet implemented"
	@exit 1

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all test test-vectors clean
