# Academic Micro Project Report: Container Virtualization & Microservice Orchestration

**Project Title:** Cloud Virtualization & Container Orchestration Dashboard with Docker Engine, Nginx Reverse Proxy, and Kubernetes  
**Subject:** Docker & Container Virtualization (Cloud Computing / DevOps)  
**Academic Year:** 2026  

---

## 1. Abstract & Executive Summary

Virtualization has evolved from heavyweight hardware-level virtual machines (hypervisors) to lightweight operating-system-level virtualization (containers). This micro-project demonstrates the architecture, deployment, and management of a containerized multi-tier enterprise CRUD dashboard.

The system features:
1. **Docker Engine Virtualization:** Utilizing Linux Namespaces (PID, NET, MNT, IPC, UTS) and Control Groups (cgroups v2) for process and resource isolation.
2. **Layer-7 Edge Reverse Proxying (Nginx):** Directing traffic from port 80/443 to internal upstream WSGI application containers (`web:8000`), terminating SSL, and offloading static assets using Linux kernel `sendfile`.
3. **Multi-Container Orchestration (Docker Compose):** Coordinating interconnected services (`web`, `nginx`, `db`) with automated health checks, isolated bridge networks, and persistent storage volumes.
4. **Declarative Kubernetes Orchestration (K8s):** Scalable deployments with replica sets, automated rolling updates, self-healing, PersistentVolumeClaims, Ingress routing, and Horizontal Pod Autoscalers (HPA).
5. **Interactive DevOps Management Dashboard:** An integrated web dashboard allowing real-time monitoring and CRUD operations on containers, inspection of Docker Engine metrics, and dynamic pod scaling.

---

## 2. Architectural Blueprint

```
+-----------------------------------------------------------------------------------+
|                                Client Web Browser                                 |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ [HTTP Port 80 / 8080]
+───────────────────────────────────────────────────────────────────────────────────+
|               NGINX REVERSE PROXY CONTAINER (ems-nginx-proxy)                     |
|                                                                                   |
|   ┌────────────────────────────────┐         ┌────────────────────────────────┐   |
|   |   Static Assets Route (/static/)  |         |   Dynamic Pass (proxy_pass /)  |   |
|   |   Direct Volume Read /sendfile |         |   Pass to Upstream web:8000    |   |
|   └───────────────┬────────────────┘         └───────────────┬────────────────┘   |
+───────────────────┼──────────────────────────────────────────┼────────────────────+
                    │ (Volume Mount)                           │ (TCP Virtual Net)
                    ▼                                          ▼
+─────────────────────────────────────+    +────────────────────────────────────────+
|       DOCKER SHARED VOLUMES         |    |      DJANGO GUNICORN APP CONTAINER     |
|   - static_volume (/app/staticfiles)|    |              (ems-web-app)             |
|   - media_volume  (/app/media)      |    |                                        |
+─────────────────────────────────────+    |  - WSGI Gunicorn Workers (Port 8000)   |
                                           |  - Docker Engine SDK Connector         |
                                           |  - Health Probe: /api/health/          |
                                           +───────────────────┬────────────────────+
                                                               │ (Port 3306)
                                                               ▼
                                           +────────────────────────────────────────+
                                           |       MYSQL DATABASE CONTAINER         |
                                           |             (ems-mysql-db)             |
                                           |                                        |
                                           |  - MySQL 8.0 InnoDB Engine             |
                                           |  - Persistent Volume: ems_mysql_data   |
                                           +────────────────────────────────────────+
```

---

## 3. Core Virtualization Concepts Demonstrated

### 3.1 OS-Level Virtualization vs Hardware Virtual Machines

| Feature | Type-2 Hypervisors (VirtualBox / VMware) | Docker Containers (runc / containerd) |
| :--- | :--- | :--- |
| **Virtualization Layer** | Hardware abstraction (hypervisor) | Kernel abstraction (Namespaces & Cgroups) |
| **Guest OS** | Full redundant OS kernel per VM | Shares host Linux kernel; isolated user space |
| **Boot Duration** | 45 - 120 seconds | Under 1 second (instant process fork) |
| **Memory Footprint** | 2GB - 8GB per instance | 50MB - 250MB per container |
| **Disk Storage** | Heavy VM disk image files (.vdi/.vmdk) | Layered UnionFS (OverlayFS) with Copy-on-Write |

### 3.2 Linux Kernel Isolation Primitives

1. **PID Namespace:** Isolates the process ID space. The main Gunicorn process appears as PID 1 inside the container, preventing visibility into host processes.
2. **NET Namespace:** Grants each container an independent network stack, loopback device, IP address (`172.20.0.x`), and routing table.
3. **MNT (Mount) Namespace:** Provides a private view of file system mount points via OverlayFS.
4. **UTS Namespace:** Isolates hostnames and NIS domain names (`ems-web-app`, `ems-nginx-proxy`).
5. **IPC Namespace:** Isolates Inter-Process Communication, POSIX message queues, and shared memory.
6. **Control Groups (cgroups v2):** Enforces hard resource limits (e.g., maximum 1.0 vCPU and 512 MB memory), preventing "noisy neighbor" resource starvation.

---

## 4. Technology Stack & Component Breakdown

- **Web Application & API:** Python 3.11, Django 5.x, Django REST Framework, Gunicorn WSGI.
- **Reverse Proxy & Ingress:** Nginx 1.25 Alpine (Layer-7 Load Balancer, SSL Termination, Static Caching).
- **Virtualization Engine:** Docker Engine (Server Version 29.8+), containerd, runc.
- **Container Orchestration:** Docker Compose v2 & Kubernetes (k8s v1.30+).
- **Database System:** MySQL 8.0 with utf8mb4 charset and Persistent Volume Claim storage.
- **Frontend Presentation:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons.

---

## 5. Deployment Instructions

### Method A: Running via Docker Compose (Recommended)

1. Open a terminal in the project directory:
   ```bash
   cd F:\employee
   ```
2. Build and launch all container services:
   ```bash
   docker compose up -d --build
   ```
3. Inspect running containers and networks:
   ```bash
   docker compose ps
   ```
4. Access the services in your browser:
   - **Application (via Nginx Reverse Proxy):** `http://localhost:80`
   - **DevOps Virtualization Dashboard:** `http://localhost:80/devops/`
   - **Docker Containers CRUD:** `http://localhost:80/devops/containers/`
   - **Kubernetes Cluster Monitor:** `http://localhost:80/devops/kubernetes/`
   - **Nginx Route Inspector:** `http://localhost:80/devops/nginx/`
   - **Health Probe:** `http://localhost:80/api/health/`

### Method B: Deploying to a Kubernetes Cluster

1. Apply all manifests in the `k8s/` directory:
   ```bash
   kubectl apply -f k8s/
   ```
2. Check pod and service status:
   ```bash
   kubectl get pods,svc,pvc,ingress -n microproject-virtualization
   ```
3. Access via the NodePort service at: `http://localhost:30080`

### Method C: Local Standalone Development (Zero-Config SQLite)

1. Run the local launcher:
   ```cmd
   run-local.bat
   ```
   Or manually:
   ```bash
   python manage.py migrate
   python seed_data.py
   python manage.py runserver 0.0.0.0:8000
   ```

---

## 6. Pre-Configured Demo Credentials

| Role | Username | Password | Access Privileges |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Full access to DevOps dashboard, container controls, and Django admin |
| **HR Manager** | `hrmanager` | `Password@123` | Employee management, payroll creation, leave approvals |

---

## 7. Viva Voce Questions & Answers

### Q1: What is the purpose of Docker's multi-stage build in this project?
**Answer:** The multi-stage `Dockerfile` uses a `builder` stage with compilation tools (`gcc`, `default-libmysqlclient-dev`) to compile Python wheels. The second stage copies only the built wheels into a minimal `python:3.11-slim` runtime image. This eliminates build tools, compilers, and cache files from the final container, drastically reducing image size from ~900MB to ~180MB and minimizing the attack surface.

### Q2: Why is Nginx placed in front of Gunicorn instead of exposing Gunicorn directly?
**Answer:** 
1. **Security Isolation:** Gunicorn is not designed to face direct untrusted internet traffic. Nginx mitigates slowloris and DDoS attacks.
2. **Performance:** Nginx uses asynchronous event-driven I/O to serve static and media files directly from shared Docker volumes without waking up Python workers.
3. **Buffering & Keep-Alive:** Nginx buffers slow client requests and sends fast, complete payloads to Gunicorn workers.

### Q3: How is data persistence handled when a container is removed?
**Answer:** Docker containers have an ephemeral writable layer (Copy-on-Write). When a container is removed, changes inside that layer are deleted. To ensure database durability, we mount a **Docker Named Volume** (`mysql_data:/var/lib/mysql`) or a Kubernetes **PersistentVolumeClaim (PVC)**. The database files live on the host filesystem outside the container life cycle.

### Q4: What are Kubernetes Readiness and Liveness Probes?
**Answer:**
- **Liveness Probe:** Periodically checks if the container is still running. If `/api/health/` returns an error or fails to respond, kubelet restarts the container.
- **Readiness Probe:** Determines whether the container is ready to accept incoming user traffic. Only when `/api/health/` returns HTTP 200 does Kubernetes route network traffic through the Service to that Pod.

### Q5: How do containers communicate with each other in Docker Compose?
**Answer:** Docker Compose creates a user-defined bridge network (`ems_virtualization_net`). Docker's embedded DNS server automatically resolves container service names (e.g., `db`, `web`, `nginx`) to their respective private container IP addresses without hardcoding IPs.

