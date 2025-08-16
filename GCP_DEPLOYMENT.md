# Google Cloud Platform Deployment Guide for ATM System

## 🚀 Deployment Options

### **Option 1: Google App Engine (Recommended)**

**Pros:** Easiest, automatic scaling, managed environment, generous free tier
**Cons:** Platform-specific limitations

#### **Step 1: Prepare Your Project**
Your project is already prepared with:
- ✅ `requirements.txt` (includes gunicorn)
- ✅ Flask app ready for production

#### **Step 2: Create app.yaml for App Engine**
Create `app.yaml` file:
```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

instance_class: F1

automatic_scaling:
  target_cpu_utilization: 0.6
  min_instances: 1
  max_instances: 10

env_variables:
  FLASK_ENV: production
  FLASK_DEBUG: "false"
```

#### **Step 3: Create Google Cloud Account**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create account (free tier available)
3. Set up billing and security

#### **Step 4: Install Google Cloud CLI**
```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install

# Or using PowerShell (Windows):
# Download and run the installer from Google Cloud website
```

#### **Step 5: Initialize and Deploy**
```bash
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create atm-system-project --name="ATM System"

# Set the project
gcloud config set project atm-system-project

# Enable App Engine API
gcloud services enable appengine.googleapis.com

# Deploy to App Engine
gcloud app deploy

# Open the deployed app
gcloud app browse
```

#### **Step 6: Access Your Deployed App**
- Your app will be available at: `https://your-project-id.appspot.com`
- Test with: `curl -X GET https://your-project-id.appspot.com/accounts/123456789/balance`

---

### **Option 2: Google Cloud Run (Serverless)**

**Pros:** Pay per request, auto-scaling, container-based
**Cons:** Cold starts, more complex setup

#### **Step 1: Create Dockerfile**
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

#### **Step 2: Build and Deploy**
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Build and push container
gcloud builds submit --tag gcr.io/your-project-id/atm-system

# Deploy to Cloud Run
gcloud run deploy atm-system \
  --image gcr.io/your-project-id/atm-system \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

#### **Step 3: Access Your Deployed App**
- Your app will be available at the URL provided by Cloud Run
- Test with: `curl -X GET https://your-service-url/accounts/123456789/balance`

---

### **Option 3: Google Compute Engine (VMs)**

**Pros:** Full control, cheaper for high-traffic apps
**Cons:** More complex setup, manual management

#### **Step 1: Create VM Instance**
```bash
# Create VM instance
gcloud compute instances create atm-system-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server,https-server

# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags=http-server \
  --description="Allow HTTP traffic"

# Allow custom port
gcloud compute firewall-rules create allow-custom \
  --allow tcp:5000 \
  --target-tags=http-server \
  --description="Allow custom port"
```

#### **Step 2: Connect to VM**
```bash
# Connect via SSH
gcloud compute ssh atm-system-vm --zone=us-central1-a
```

#### **Step 3: Install Dependencies**
```bash
# Update system
sudo apt-get update

# Install Python and pip
sudo apt-get install python3 python3-pip -y

# Install git (optional)
sudo apt-get install git -y
```

#### **Step 4: Deploy Your Code**
```bash
# Create app directory
mkdir atm-system
cd atm-system

# Upload your files (use gcloud scp or copy-paste)
# Option A: Using gcloud scp
gcloud compute scp --recurse "C:\Users\yaira\Desktop\ATM System Project\*" atm-system-vm:~/atm-system/ --zone=us-central1-a

# Option B: Clone from GitHub (if you push to GitHub)
git clone https://github.com/yourusername/atm-system.git
```

#### **Step 5: Install Python Dependencies**
```bash
cd atm-system
pip3 install -r requirements.txt
```

#### **Step 6: Run the Application**
```bash
# Test run
python3 app.py

# For production (background)
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app &
```

#### **Step 7: Set Up Domain (Optional)**
```bash
# Install nginx for reverse proxy
sudo apt-get install nginx -y

# Configure nginx
sudo nano /etc/nginx/sites-available/atm-system
```

Add to nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/atm-system /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔧 Post-Deployment Configuration

### **Environment Variables**
```bash
# For App Engine, add in app.yaml:
env_variables:
  FLASK_ENV: production
  FLASK_DEBUG: "false"
```

### **Custom Domain (Optional)**
1. **Buy domain** from Google Domains or external provider
2. **Create SSL certificate** (automatic with App Engine)
3. **Configure DNS** to point to your deployment
4. **Map custom domain** in App Engine settings

### **Monitoring and Logs**
- **Cloud Logging**: Monitor application logs
- **Cloud Monitoring**: Set up alerts and dashboards
- **Error Reporting**: Track application errors

---

## 🧪 Testing Your Deployment

### **Test Basic Functionality**
```bash
# Get balance
curl -X GET https://your-app-url/accounts/123456789/balance

# Deposit money
curl -X POST https://your-app-url/accounts/123456789/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 100.00}'

# Withdraw money
curl -X POST https://your-app-url/accounts/123456789/withdraw \
-H "Content-Type: application/json" \
-d '{"amount": 50.00}'
```

### **Test Concurrent Access**
```bash
# Upload test_concurrent.py to your server
python3 test_concurrent.py
```

---

## 💰 Cost Estimation

### **App Engine**
- **Free tier**: 28 instance hours/day, 5GB storage, 1GB/day outbound
- **After free tier**: ~$5-20/month for small app

### **Cloud Run**
- **Free tier**: 2M requests/month, 360,000 vCPU-seconds, 180,000 GiB-seconds
- **After free tier**: ~$1-10/month for small app

### **Compute Engine**
- **Free tier**: 1 f1-micro instance/month
- **After free tier**: ~$5-15/month for e2-micro

---

## 🚨 Security Considerations

1. **IAM Roles**: Use least privilege principle
2. **HTTPS**: Automatic with App Engine and Cloud Run
3. **Environment Variables**: Don't hardcode secrets
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Set up Cloud Monitoring alerts

---

## 📞 Need Help?

- **Google Cloud Documentation**: [App Engine](https://cloud.google.com/appengine/docs)
- **Google Cloud Support**: Available with paid plans
- **Community**: Google Cloud Community and Stack Overflow

---

## 🎯 Quick Start Commands

```bash
# 1. Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login and setup
gcloud auth login
gcloud projects create atm-system-project
gcloud config set project atm-system-project

# 3. Enable APIs
gcloud services enable appengine.googleapis.com

# 4. Deploy
gcloud app deploy

# 5. Open app
gcloud app browse
```
