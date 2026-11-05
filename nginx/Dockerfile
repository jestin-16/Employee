FROM nginx:1.25-alpine

LABEL maintainer="Student <student@university.edu>"
LABEL description="Nginx Reverse Proxy & Load Balancer for Micro Project"

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom reverse proxy configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create static directories
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]

