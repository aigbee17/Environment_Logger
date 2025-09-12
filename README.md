# Environment Logger

## Overview

Environment Logger is an educational project developed as an introduction to embedded systems and cross-language integration. This repository demonstrates essential concepts in embedded programming, system interfacing, and basic web API design using a combination of C, Python (FastAPI), Docker, and SQLite. It was created to help me learn and explore how low-level sensor interfacing can connect with modern software architecture.

**Note:** This codebase is intended for instructional and demonstration purposes only. It is not designed for deployment in production environments or for use with live sensor hardware.

## Key Components

- **C Modules:** Explore sensor data collection techniques and basic hardware interfacing.
- **Python FastAPI Service:** Provides a simple web API for interacting with stored environmental data.
- **SQLite Database:** Serves as a lightweight storage solution for logged readings.
- **Docker Integration:** Enables consistent and straightforward environment setup across platforms.


## Getting Started

### Prerequisites

- Docker (recommended for setup)
- Python 3.x (if running without Docker)
- GCC or compatible C compiler (for building sensor simulation modules)


## Usage

- The project simulates sensor readings via C code, which are then logged into a local SQLite database.
- The FastAPI web service exposes endpoints for querying logged data.
- The included Docker setup ensures easy reproducibility of the demo environment.

## Educational Objectives

- Introduce basic sensor interfacing with C.
- Demonstrate cross-language communication between C and Python.
- Model basic web API development and database integration.
- Showcase best practices for containerized development and experimentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Developed by [@aigbee17](https://github.com/aigbee17)  
