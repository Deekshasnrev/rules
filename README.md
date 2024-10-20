# **Weather Monitoring Application**

## Overview

This application fetches weather data for specified cities from the OpenWeatherMap API and displays the information on a web interface. It also includes features for alerting based on user-configurable thresholds such as temperature and weather conditions. This document provides comprehensive build instructions, design choices, and dependency setup for the application.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Design Choices](#design-choices)
3. [Dependencies](#dependencies)
4. [Installation and Setup](#installation-and-setup)
---

## **1. Overview**

The Weather Monitoring Application allows users to view real-time weather data for various cities and visualize historical trends. It supports the following features:
- Fetches weather data dynamically using the OpenWeatherMap API.
- Visualizes the data using a user-friendly chart.
- Allows users to set up temperature and weather condition thresholds.
- Triggers alerts when these thresholds are exceeded.

---

## **2. Design Choices**

1. **Django Framework:** The application uses Django for its robustness, scalability, and ease of integrating with databases and external APIs.
2. **PostgreSQL Database:** The choice of PostgreSQL was made due to its reliability and extensive feature set that supports complex queries, which are useful for fetching historical weather data.
3. **Chart.js Library:** Chart.js is used for rendering interactive and responsive charts to visualize weather trends. It is lightweight and integrates well with JavaScript.
4. **Docker:** Docker containers are used to package the application and its dependencies, ensuring consistency across different environments (development, testing, and production).
5. **Logging System:** Python's logging library is used for monitoring and debugging purposes. Logs capture threshold breaches and application errors.

---

## **3. Dependencies**

Before running the application, ensure the following dependencies are installed:

### **Backend Dependencies**

- **Django (>= 4.0)**: Python web framework for building the backend.
- **Django REST Framework (>= 3.12)**: For building API endpoints.
- **Requests Library (>= 2.26)**: For making HTTP requests to the OpenWeatherMap API.
- **PostgreSQL (>= 13)**: Database system for storing weather data and user-configured thresholds.

### **Frontend Dependencies**

- **Bootstrap (>= 5.1)**: For styling the frontend.
- **Chart.js (>= 3.7)**: For data visualization.
- **jQuery (>= 3.6)**: Simplifies frontend scripting and AJAX calls.

### **Docker Dependencies**

- **Docker**: Ensure Docker is installed on your system to run the application in a containerized environment.
- **Docker Compose**: Used to set up multiple containers (Django app, PostgreSQL, etc.).

---

## **4. Installation and Setup**

### **4.1 Setting up the Environment**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Deekshasnrev/weather-monitor.git
   cd weather-monitoring-app
