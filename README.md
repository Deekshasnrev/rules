# **Rules Evaluation Application**

## Overview

This application evaluates user-defined rules based on various attributes such as age, salary, and department. The rules are defined using logical operators and are evaluated dynamically. It allows users to create, modify, and combine rules in a user-friendly interface. This document provides comprehensive build instructions, design choices, and dependency setup for the application.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Design Choices](#design-choices)
3. [Dependencies](#dependencies)
4. [Installation and Setup](#installation-and-setup)
5. [Guide](#Guide)
---

## **1. Overview**

The Rules Evaluation Application enables users to create and manage dynamic rules, which are evaluated against user attributes. It supports the following features:
- Rule creation using logical operators (AND, OR, etc.).
- Dynamic evaluation of rules using Abstract Syntax Tree (AST).
- Custom admin portal for managing rules and evaluations.
- Modular design allowing easy scalability and integration of additional rule types.

---

## **2. Design Choices**

1. **Django Framework:** The application leverages Django for its modularity and rapid development capabilities, making it easy to integrate complex backend logic.
2. **Abstract Syntax Tree (AST) for Rules:** The AST structure is used to represent and evaluate rules efficiently, allowing flexible combinations of rules at runtime.
3. **Custom Admin Portal:** Instead of using Django's built-in admin, a custom interface is provided to manage rules and user attributes dynamically.
4. **Docker:** Docker containers ensure consistency and reliability across different environments, from development to production.
5. **Logging System:** A comprehensive logging system is in place to capture rule evaluation results, errors, and debugging information for better monitoring.

---

## **3. Dependencies**

Before running the application, ensure the following dependencies are installed:

### **Backend Dependencies**

- **Django (>= 4.0)**: Python web framework for building the backend logic.
- **Django REST Framework (>= 3.12)**: For building API endpoints that handle rule evaluations.
- **AST (Abstract Syntax Tree)**: Core Python library for parsing and managing rule evaluation structures.
- **PostgreSQL (>= 13)**: Database system for storing user attributes and rule definitions.

### **Frontend Dependencies**

- **Bootstrap (>= 5.1)**: For building a responsive user interface.
- **jQuery (>= 3.6)**: For handling frontend scripting and dynamic form updates.
- **DataTables (>= 1.11)**: Provides dynamic, interactive tables for displaying rules and evaluations.

### **Docker Dependencies**

- **Docker**: Ensure Docker is installed on your system to run the application in a containerized environment.
- **Docker Compose**: Used to orchestrate multiple containers (Django app, PostgreSQL, etc.).

---

## **4. Installation and Setup**

### **4.1 Setting up the Environment**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Deekshasnrev/rules.git
   cd rules
   cd rule_engine

2.  **Make sure the manage.py file is present there , otherwise go that folder**
3.  **Start the server**
    ```bash
    python manage.py runserver
 4. **Go thr link which comes Eg:'http://127.0.0.1:8000/'**

## Guide

# First enter '/engine/' in the url then enter '/create-rule/'

![Screenshot 2024-10-20 235611](https://github.com/user-attachments/assets/06f632cd-bb19-4720-842f-e2fb101d008c)


![Screenshot 2024-10-20 235639](https://github.com/user-attachments/assets/b838f085-b962-4249-b73d-782577c55997)


# Now enter the rules you want to create in the textbox (it is case sensitive , write operands in small cases eg-age,salary and operans in capital cases eg-AND,OR) , it will show error if there is any invalid inputs

![Screenshot 2024-10-20 235712](https://github.com/user-attachments/assets/04ed4853-712a-41a5-bb6e-8840a3267cb3)

# As we have create our first rule , Click on Evaluate rule button to evaluate it . Then write the condition only in JSON format.

![Screenshot 2024-10-20 235737](https://github.com/user-attachments/assets/8940552c-d049-435c-9a95-128bd98d8757)

# We can combine the ruls also by clicking on Combine rules button , write the rules you want to combine line by line with operands if needed otherwise it will consider as 'OR'

![Screenshot 2024-10-20 235817](https://github.com/user-attachments/assets/0dc54fc0-a3ff-4c11-b9ee-4eb8a21de363)

# And same we can evaluate the combined rule also by clicking on Evaluate rule and writing input in JSON format 

![Screenshot 2024-10-20 235908](https://github.com/user-attachments/assets/e120e57f-a85f-495d-a439-755d68f1a8aa)


# All the written rules will be saved in Database (SQLite3)


