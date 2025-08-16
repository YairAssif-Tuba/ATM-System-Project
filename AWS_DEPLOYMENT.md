# AWS Deployment Guide for ATM System

## 🚀 Deployment Options

### **Option 1: AWS Elastic Beanstalk (Recommended)**

**Pros:** Easiest, automatic scaling, managed environment
**Cons:** Slightly more expensive

#### **Step 1: Prepare Your Project**
Your project is already prepared with:
- ✅ `requirements.txt` (includes gunicorn)
- ✅ `Procfile` (web: gunicorn app:app)
- ✅ Flask app ready for production

#### **Step 2: Create AWS Account**
1. Go to [AWS Console](https://aws.amazon.com/)
2. Create account (free tier available)
3. Set up billing and security

#### **Step 3: Deploy via AWS Console**
1. **Go to Elastic Beanstalk Console**
   - Search "Elastic Beanstalk" in AWS Console
   - Click "Create Application"

2. **Configure Application**
   ```
   Application name: atm-system
   Platform: Python
   Platform branch: Python 3.9
   Platform version: 3.9.16
   ```

3. **Upload Code**
   - Create a ZIP file of your project:
   ```bash
   # On Windows PowerShell:
   Compress-Archive -Path "app.py", "requirements.txt", "Procfile", "test_api.py", "test_concurrent.py" -DestinationPath "atm-system.zip"
   ```
   - Upload the ZIP file

4. **Configure Environment**
   - Environment name: `atm-system-prod`
   - Domain: `atm-system-prod.elasticbeanstalk.com` (or custom)

5. **Click "Create Environment"**

#### **Step 4: Access Your Deployed App**
- Your app will be available at: `http://your-app-name.elasticbeanstalk.com`
- Test with: `curl -X GET http://your-app-name.elasticbeanstalk.com/accounts/123456789/balance`

---

### **Option 2: AWS EC2 (More Control)**

**Pros:** Full control, cheaper for small apps
**Cons:** More complex setup

#### **Step 1: Launch EC2 Instance**
1. **Go to EC2 Console**
   - Search "EC2" in AWS Console
   - Click "Launch Instance"

2. **Choose Instance Type**
   ```
   Name: atm-system-server
   AMI: Amazon Linux 2023
   Instance type: t2.micro (free tier)
   Key pair: Create new (download .pem file)
   Security Group: Create new
   ```

3. **Configure Security Group**
   ```
   SSH (22): 0.0.0.0/0 (your IP only)
   HTTP (80): 0.0.0.0/0
   Custom TCP (5000): 0.0.0.0/0
   ```

#### **Step 2: Connect to Instance**
```bash
# On Windows, use PuTTY or PowerShell:
ssh -i "your-key.pem" ec2-user@your-instance-public-ip
```

#### **Step 3: Install Dependencies**
```bash
# Update system
sudo yum update -y

# Install Python 3.9
sudo yum install python3 python3-pip -y

# Install git (optional)
sudo yum install git -y
```

#### **Step 4: Deploy Your Code**
```bash
# Create app directory
mkdir atm-system
cd atm-system

# Upload your files (use scp or copy-paste)
# Option A: Using scp from your local machine
scp -i "your-key.pem" -r "C:\Users\yaira\Desktop\ATM System Project\*" ec2-user@your-instance-public-ip:~/atm-system/

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
sudo yum install nginx -y

# Configure nginx
sudo nano /etc/nginx/nginx.conf
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
# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

### **Option 3: AWS Lambda + API Gateway (Serverless)**

**Pros:** Pay per request, auto-scaling
**Cons:** More complex, cold starts

#### **Step 1: Modify App for Lambda**
Create `lambda_handler.py`:
```python
from app import app

def lambda_handler(event, context):
    return app(event, context)
```

#### **Step 2: Create Deployment Package**
```bash
pip install -r requirements.txt -t .
zip -r lambda-deployment.zip .
```

#### **Step 3: Deploy via AWS Console**
1. Create Lambda function
2. Upload ZIP file
3. Configure API Gateway
4. Set up routes

---

## 🔧 Post-Deployment Configuration

### **Environment Variables (Optional)**
```bash
# For Elastic Beanstalk, add in console:
FLASK_ENV=production
FLASK_DEBUG=False
```

### **Custom Domain (Optional)**
1. **Buy domain** from Route 53 or external provider
2. **Create SSL certificate** in AWS Certificate Manager
3. **Configure DNS** to point to your deployment
4. **Update security groups** for HTTPS (443)

### **Monitoring and Logs**
- **CloudWatch**: Monitor application logs
- **X-Ray**: Trace requests (optional)
- **Health checks**: Configure in Elastic Beanstalk

---

## 🧪 Testing Your Deployment

### **Test Basic Functionality**
```bash
# Get balance
curl -X GET http://your-app-url/accounts/123456789/balance

# Deposit money
curl -X POST http://your-app-url/accounts/123456789/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 100.00}'

# Withdraw money
curl -X POST http://your-app-url/accounts/123456789/withdraw \
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

### **Elastic Beanstalk**
- **Free tier**: 750 hours/month for 12 months
- **After free tier**: ~$15-30/month for small app

### **EC2**
- **Free tier**: 750 hours/month for 12 months
- **After free tier**: ~$8-15/month for t2.micro

### **Lambda**
- **Free tier**: 1M requests/month
- **After free tier**: ~$1-5/month for small app

---

## 🚨 Security Considerations

1. **Update Security Groups**: Only allow necessary ports
2. **Use HTTPS**: Configure SSL certificates
3. **Environment Variables**: Don't hardcode secrets
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Set up CloudWatch alerts

---

## 📞 Need Help?

- **AWS Documentation**: [Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- **AWS Support**: Available with paid plans
- **Community**: AWS Forums and Stack Overflow
