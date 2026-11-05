@echo off
echo ===============================================================================
echo   Kubernetes Cluster Deployment - Container Virtualization Micro Project
echo ===============================================================================
echo.
echo 1. Applying declarative Kubernetes manifests using Kustomize...
kubectl apply -k k8s/

echo.
echo 2. Checking deployment status in namespace 'microproject-virtualization'...
kubectl get pods,svc,pvc,ingress -n microproject-virtualization

echo.
echo ===============================================================================
echo   Kubernetes workloads successfully scheduled!
echo   NodePort URL: http://localhost:30080
echo ===============================================================================
pause
