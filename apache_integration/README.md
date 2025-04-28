# Apache Integration for Fiona Chatbot

This module provides instructions and configuration for integrating the Fiona Chatbot solution into an existing Apache2 and PHP (8.x) environment.

---

## Prerequisites
1. Apache2 installed on your server.
2. PHP (8.x) installed if needed for other parts of your application.
3. Docker installed to run the backend and frontend services.

---

## Step 1: Configure Apache
1. Copy the `apache_config` file to the Apache sites-available directory:
   ```bash
   sudo cp apache_config /etc/apache2/sites-available/fiona-chatbot.conf
   ```

2. Enable the site and required modules:
   ```bash
   sudo a2ensite fiona-chatbot.conf
   sudo a2enmod proxy proxy_http rewrite headers
   sudo systemctl reload apache2
   ```

---

## Step 2: Deploy the Frontend
1. Build the React frontend:
   ```bash
   cd frontend
   npm run build
   ```
2. Copy the build files to the Apache document root:
   ```bash
   sudo cp -r build/ /var/www/fiona-chatbot/frontend
   ```

---

## Step 3: Deploy the Backend
1. Start the backend using Docker:
   ```bash
   cd backend
   docker-compose up -d
   ```
2. Ensure the backend is running on `http://127.0.0.1:8000`.

---

## Step 4: Test the Integration
1. Access the frontend at `http://your-domain.com`.
2. Ensure API requests (e.g., `/api/query`) are proxied to the backend.

---

## Optional: Secure with HTTPS
Use Let's Encrypt to secure your site with HTTPS:
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d your-domain.com
```

---

This setup ensures that Apache serves the frontend and proxies API requests to the backend, integrating seamlessly into an Apache2 and PHP (8.x) environment.