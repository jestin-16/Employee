# PeopleCore — Employee Management System (EMS) 🚀
### Container Virtualization & Microservice Orchestration Micro Project

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Engine_29.x-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-K8s_Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Architectural Blueprint](#-architectural-blueprint)
3. [Key Modules & Features](#-key-modules--features)
4. [Container Virtualization & Cloud-Native Stack](#-container-virtualization--cloud-native-stack)
5. [Quick Start & Running Guide](#-quick-start--running-guide)
   - [Option 1: Docker Compose (Recommended)](#option-1-docker-compose-full-stack)
   - [Option 2: Kubernetes Cluster Deployment](#option-2-kubernetes-cluster-deployment)
   - [Option 3: Local Development (Zero-Config SQLite)](#option-3-local-development-zero-config-sqlite)
6. [Access Endpoints & Network Topology](#-access-endpoints--network-topology)
7. [Default Credentials](#-default-credentials)
8. [Health Check Probes & Monitoring](#-health-check-probes--monitoring)
9. [Project Directory Structure](#-project-directory-structure)
10. [Academic Micro-Project Concepts Covered](#-academic-micro-project-concepts-covered)

---

## 🌟 Overview

**PeopleCore** is a modern, enterprise **Employee Management System (EMS)** designed for modern workforce administration. Behind its sleek, minimalistic Scandinavian/Linear-inspired user interface lies a **cloud-native, multi-tier container virtualization architecture** powered by **Docker Engine**, **Nginx Reverse Proxy**, and **Kubernetes**.

### Highlights
- **Aesthetic Minimalist UI**: Clean obsidian sidebar, soft card elevations, Plus Jakarta Sans typography, staggered card entrances, live status pulse glows, and animated count-up numbers.
- **Enterprise CRUD Capabilities**: Comprehensive management for staff records, organizational hierarchies, leave workflows, daily attendance, and monthly payroll disbursement.
- **Production Containerization**: Multi-stage lightweight Docker image (`python:3.11-slim`), isolated unprivileged runtime user (`appuser`), shared persistent volumes, and health check probes.
- **Layer-7 Edge Reverse Proxy**: High-performance Nginx routing, kernel `sendfile` static/media asset offloading, Gzip compression, and dynamic upstream proxying with full CSRF origin preservation.
- **Zero-Friction Dual Database Support**: Seamlessly shifts between containerized **MySQL 8.0** and local **SQLite3** without configuration overhead.

---

## 🏗️ Architectural Blueprint

```
                                  +-----------------------+
                                  |  Client Web Browser   |
                                  +-----------+-----------+
                                              |
                                              | HTTP Port 8088
                                              v
               +-------------------------------------------------------------+
               |         NGINX REVERSE PROXY CONTAINER (ems-nginx-proxy)     |
               |                                                             |
               |   +--------------------------+  +------------------------+  |
               |   |   Static Offload Route   |  |   Dynamic Pass (/)     |  |
               |   |   /static/ and /media/   |  |   Upstream web:8000    |  |
               |   +------------+-------------+  +-----------+------------+  |
               +----------------|----------------------------|---------------+
                                | (Volume Mount)             | (Bridge Network)
                                v                            v
    +------------------------------------+    +------------------------------+
    |       DOCKER SHARED VOLUMES        |    |   DJANGO GUNICORN CONTAINER  |
    |   - ems_static_volume (/app/static)|    |         (ems-web-app)        |
    |   - ems_media_volume  (/app/media) |    |                              |
    +------------------------------------+    |   * Python 3.11 + Gunicorn   |
                                              |   * REST Health: /api/health |
                                              +--------------+---------------+
                                                             | Port 3306
                                                             v
                                              +------------------------------+
                                              |   MYSQL DATABASE CONTAINER   |
                                              |         (ems-mysql-db)       |
                                              |                              |
                                              |   * Persistent ems_mysql_data|
                                              |   * Strict SQL Mode UTF-8    |
                                              +------------------------------+
```

---

## 💼 Key Modules & Features

| Module | Features & Capabilities |
| :--- | :--- |
| **Workforce Directory** | Full CRUD for employee records, avatar initials, department assignment, designation, emergency contacts, hire date, and active/on-leave status toggles. |
| **Department Structure** | Create and organize operational departments, set department heads, view headcount distributions, and track budget allocations. |
| **Leave Management** | Employee leave application workflow (Casual, Sick, Annual, Maternity), status lifecycle (`Pending`, `Approved`, `Rejected`), and manager action controls. |
| **Daily Attendance** | Mark daily clock-in / clock-out times, track working hours, monitor `Present`, `Late`, `Absent`, or `Half-Day` status. |
| **Payroll Processing** | Automated salary calculation, allowance management, tax/deduction tracking, payment status (`Draft`, `Approved`, `Paid`), and disbursement logging. |
| **Company Bulletins** | Internal bulletin board for broadcasting organizational updates, policy changes, and team announcements. |
| **Aesthetic Dashboard** | Interactive metrics counter, operational team status, real-time bulletins feed, and animated quick-action shortcuts. |

---

## ⚙️ Container Virtualization & Cloud-Native Stack

### 1. Docker Engine Virtualization
- **Multi-Stage Build (`Dockerfile`)**: Builder stage compiles C-wheels for MySQL client libraries; runtime stage uses `python:3.11-slim` with stripped build tools for minimal image footprint (~180MB) and hardened security.
- **Non-Root Execution**: Runs under unprivileged `appuser` (UID 1001) adhering to the Principle of Least Privilege.
- **Docker Healthchecks**: Automatic container health monitoring testing `/api/health/` endpoints.

### 2. Multi-Container Orchestration (`docker-compose.yml`)
- **Service Mesh**: Coordinates `db` (MySQL 8), `web` (Django Gunicorn), and `nginx` (Reverse Proxy).
- **Network Virtualization**: Isolated user-defined bridge network (`ems_virtualization_net`) providing automatic container DNS resolution.
- **Storage Virtualization**: Named persistent volumes (`ems_mysql_data`, `ems_static_volume`, `ems_media_volume`).

### 3. Edge Reverse Proxy & Offloader (`nginx/nginx.conf`)
- **Layer-7 Reverse Proxying**: Routes port 8088 traffic to internal `web:8000`.
- **Static Asset Offloading**: Bypasses Python runtime completely for `/static/` and `/media/` using Linux kernel `sendfile` and 30-day client caching.
- **Gzip Compression**: Compresses CSS, JS, JSON, and SVG payloads.
- **Header Forwarding**: Preserves client host and port via `$http_host` to guarantee CSRF origin matching.

### 4. Declarative Kubernetes Orchestration (`k8s/`)
- **Namespace Isolation**: Deployed in dedicated `microproject-virtualization` namespace.
- **ConfigMaps & Secrets**: Externalized environment variables and base64 credentials.
- **PersistentVolumeClaims (PVC)**: Reliable storage allocation for MySQL database state.
- **Deployments & Services**: Multi-replica deployments with ClusterIP and NodePort exposure.
- **Horizontal Pod Autoscaler (HPA)**: Automated scaling from 2 to 10 pods based on CPU/Memory thresholds.
- **Kustomize Integration**: Declarative single-command application with `kubectl apply -k k8s/`.

---

## 🚀 Quick Start & Running Guide

### Option 1: Docker Compose (Full Stack) — Recommended

Prerequisites: **Docker Desktop** running.

#### Windows (1-Click):
Double-click `run-docker.bat` in the project folder.

#### Terminal (macOS / Linux / Windows PowerShell):
```bash
# Clone the repository
git clone https://github.com/jestin-16/Employee.git
cd Employee

# Start all containers in the background with build
docker compose up -d --build

# Verify container status
docker compose ps
```

Once running, access the dashboard at:
👉 **[http://localhost:8088](http://localhost:8088)**

To stop the containers:
```bash
docker compose down
```

---

### Option 2: Kubernetes Cluster Deployment

Deploy the multi-tier architecture to any Kubernetes cluster (Minikube, Kind, Docker Desktop K8s, or K3s):

#### Windows (1-Click):
Double-click `deploy-k8s.bat`.

#### Terminal:
```bash
# Apply declarative Kustomize manifests
kubectl apply -k k8s/

# Monitor deployment progress
kubectl get pods,services,pvc,hpa -n microproject-virtualization
```

Access via NodePort or Ingress:
- **NodePort Service**: `http://<node-ip>:30080`
- **Ingress Controller**: `http://ems.local` (configured in `/etc/hosts`)

To tear down the Kubernetes resources:
```bash
kubectl delete -k k8s/
```

---

### Option 3: Local Development (Zero-Config SQLite)

Run directly on your local Python environment without Docker:

#### Windows (1-Click):
Double-click `run-local.bat`.

#### Terminal:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations & seed demo workforce data
python manage.py migrate
python seed_data.py

# Start Django development server
python manage.py runserver 8000
```

Access in your browser: **[http://localhost:8000](http://localhost:8000)**

---

## 🌐 Access Endpoints & Network Topology

| Component | Port | URL | Description |
| :--- | :--- | :--- | :--- |
| **Nginx Reverse Proxy** | `8088` | [http://localhost:8088](http://localhost:8088) | Primary user entry point with static offload |
| **Django WSGI Web** | `8000` | [http://localhost:8000](http://localhost:8000) | Direct Gunicorn backend application port |
| **REST Health Probe** | `8088` | [http://localhost:8088/api/health/](http://localhost:8088/api/health/) | JSON microservice health status & DB probe |
| **Nginx Stub Status** | `8088` | [http://localhost:8088/nginx_status](http://localhost:8088/nginx_status) | Active client connections & worker metrics |
| **Nginx Health Check** | `8088` | [http://localhost:8088/healthz](http://localhost:8088/healthz) | Reverse proxy liveness check |
| **Django Admin Panel** | `8088` | [http://localhost:8088/admin/](http://localhost:8088/admin/) | Underlying administrative back-office |

---

## 🔑 Default Credentials

The database comes pre-seeded with sample departments, employees, announcements, and roles:

| Account Role | Username | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full system control, admin panel, payroll disbursement |
| **HR Manager** | `hrmanager` | `Password@123` | Staff records, leave approvals, attendance logging |

---

## 🩺 Health Check Probes & Monitoring

The system exposes automated health check endpoints for container and cluster monitoring:

```bash
# Test Application & Database Health
curl http://localhost:8088/api/health/
```

**Response Payload (`HTTP 200 OK`):**
```json
{
  "status": "healthy",
  "database": "connected",
  "engine": "mysql",
  "service": "Employee Management System",
  "architecture": "Container Virtualization (Docker / Kubernetes / Nginx)"
}
```

---

## 📁 Project Directory Structure

```
Employee/
├── .dockerignore                 # Excludes cache and local files from image build
├── .env.example                  # Template configuration for environment variables
├── .gitignore                    # Git exclusions (SQLite, staticfiles, __pycache__)
├── Dockerfile                    # Multi-stage production build (Python 3.11-slim)
├── docker-compose.yml            # Multi-service configuration (web, db, nginx)
├── docker-entrypoint.sh          # Container initialization, wait-for-db & migrations
├── requirements.txt              # Production Python package dependencies
├── seed_data.py                  # Seed script populating demo workforce & admin users
├── PROJECT_REPORT.md             # Formal academic micro-project report
├── README.md                     # Comprehensive technical documentation
│
├── core/                         # Django root project configuration
│   ├── settings.py               # Dual DB support, CSRF trusted origins, WhiteNoise
│   ├── urls.py                   # Global routing and /api/health/ endpoint
│   └── wsgi.py                   # WSGI application entry for Gunicorn
│
├── employees/                    # Core business application
│   ├── models.py                 # User, Employee, Department, Leave, Attendance, Payroll
│   ├── views.py                  # Aesthetic dashboard & CRUD controllers
│   ├── forms.py                  # Crispy Bootstrap 5 forms with validation
│   ├── urls.py                   # App URL routing
│   └── templates/employees/      # Modern Scandinavian/Linear UI templates
│
├── nginx/                        # Nginx Reverse Proxy service
│   ├── Dockerfile                # Nginx Alpine container definition
│   └── nginx.conf                # Layer-7 routing, static offload, gzip, headers
│
├── k8s/                          # Kubernetes declarative deployment manifests
│   ├── 00-namespace.yaml         # Dedicated microproject namespace
│   ├── 01-configmap.yaml         # Non-confidential app environment configs
│   ├── 02-secret.yaml            # Base64 encoded credentials
│   ├── 03-mysql.yaml             # MySQL Deployment, Service & PVC
│   ├── 04-web.yaml               # Django App Deployment & Service
│   ├── 05-nginx.yaml             # Nginx Reverse Proxy Deployment & Service
│   ├── 06-ingress.yaml           # Ingress controller routing rule
│   ├── 07-hpa.yaml               # Horizontal Pod Autoscaler definition
│   └── kustomization.yaml        # Kustomize manifest bundle
│
├── templates/                    # Global base layouts
│   ├── base.html                 # Master layout (Obsidian sidebar, animations)
│   └── registration/login.html   # Minimalist authentication card
│
├── run-docker.bat / .sh          # 1-click Docker Compose launcher
├── run-local.bat                 # 1-click Local SQLite development launcher
└── deploy-k8s.bat / .sh          # 1-click Kubernetes cluster deployment script
```

---

## 🎓 Academic Micro-Project Concepts Covered

This project demonstrates practical mastery of core Cloud Computing and Container Virtualization concepts:

1. **Operating-System-Level Virtualization**: Linux Namespaces (`pid`, `net`, `mnt`, `ipc`) and Control Groups (`cgroups v2`) isolating processes without guest OS overhead.
2. **Container Build Optimization**: Multi-stage Docker builds separating compiler toolchains from runtime environments to minimize image surface and vulnerabilities.
3. **Software-Defined Networking (SDN)**: Docker isolated bridge networks enabling secure inter-container communication and container DNS service discovery.
4. **Storage Virtualization**: Decoupling ephemeral container filesystems from persistent state via Docker Named Volumes and Kubernetes `PersistentVolumeClaims`.
5. **Reverse Proxy & Edge Gateway**: High-throughput Layer-7 proxying, SSL readiness, static offloading via Linux kernel `sendfile`, and header preservation.
6. **Cloud-Native Cluster Orchestration**: Kubernetes Pod replication, declarative configuration with Kustomize, self-healing deployments, and Horizontal Pod Autoscaling (HPA).

---

## 📄 License
This project is licensed under the [MIT License](LICENSE). Built for academic and enterprise demonstration.
