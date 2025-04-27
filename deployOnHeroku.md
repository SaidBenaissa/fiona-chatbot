# Deploying Fiona Chatbot on Heroku

This guide provides step-by-step instructions to deploy the Fiona Chatbot application (backend and frontend) on Heroku using Docker.

---

## Prerequisites
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):
   ```bash
   brew tap heroku/brew && brew install heroku
   ```
2. Log in to Heroku:
   ```bash
   heroku login
   ```
3. Ensure your Heroku account is verified (add payment information if required).

---

## Step 1: Create Heroku Apps
Create separate Heroku apps for the backend and frontend:

```bash
heroku create fiona-chatbot-backend
heroku create fiona-chatbot-frontend
```

---

## Step 2: Prepare Backend for Deployment
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Set the Heroku stack to `container`:
   ```bash
   heroku stack:set container -a fiona-chatbot-backend
   ```
3. Log in to Heroku's container registry:
   ```bash
   heroku container:login
   ```
4. Build and push the backend Docker image:
   ```bash
   heroku container:push web -a fiona-chatbot-backend
   ```
5. Release the backend image:
   ```bash
   heroku container:release web -a fiona-chatbot-backend
   ```

---

## Step 3: Prepare Frontend for Deployment
1. Navigate to the `frontend/` directory:
   ```bash
   cd ../frontend
   ```
2. Set the Heroku stack to `container`:
   ```bash
   heroku stack:set container -a fiona-chatbot-frontend
   ```
3. Build and push the frontend Docker image:
   ```bash
   heroku container:push web -a fiona-chatbot-frontend
   ```
4. Release the frontend image:
   ```bash
   heroku container:release web -a fiona-chatbot-frontend
   ```

---

## Step 4: Configure Environment Variables
If the frontend needs to communicate with the backend, set the backend URL as an environment variable in the frontend app:

```bash
heroku config:set REACT_APP_BACKEND_URL=https://fiona-chatbot-backend.herokuapp.com -a fiona-chatbot-frontend
```

---

## Step 5: Verify Deployment
1. **Frontend**: Visit the frontend app URL:
   ```
   https://fiona-chatbot-frontend.herokuapp.com
   ```
2. **Backend**: Visit the backend app URL:
   ```
   https://fiona-chatbot-backend.herokuapp.com
   ```

---

## Step 6: Monitor and Scale
1. Use the Heroku dashboard to monitor your apps.
2. Scale the apps if needed:
   ```bash
   heroku ps:scale web=1 -a fiona-chatbot-backend
   heroku ps:scale web=1 -a fiona-chatbot-frontend
   ```

---

## Notes
- Ensure the `docker-compose.yml` file is not used directly on Heroku, as Heroku does not support Docker Compose.
- Monitor your Heroku free tier usage to avoid exceeding the limits.

---

This guide ensures that both the backend and frontend of the Fiona Chatbot are deployed and running on Heroku successfully.