# Heroku Deployment Guide for ATM System

## 🚀 Why Heroku?

**Pros:** 
- ✅ Extremely easy deployment
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Git-based deployment
- ✅ Great for beginners

**Cons:** 
- ❌ Free tier discontinued (but still affordable)
- ❌ Sleep mode on free tier (wakes up on first request)

## 📋 Prerequisites

1. **Git** (should be installed on your system)
2. **Heroku CLI** (we'll install this)
3. **Heroku account** (free to create)

## 🛠️ Step-by-Step Deployment

### **Step 1: Install Heroku CLI**

**Windows:**
1. Go to: https://devcenter.heroku.com/articles/heroku-cli
2. Download the Windows installer
3. Run the installer and follow the setup

**Or using PowerShell:**
```powershell
# Install via winget (Windows 10/11)
winget install --id=Heroku.HerokuCLI

# Or using Chocolatey
choco install heroku-cli
```

### **Step 2: Login to Heroku**
```bash
heroku login
```
This will open a browser window for authentication.

### **Step 3: Initialize Git Repository**
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit the changes
git commit -m "Initial commit for Heroku deployment"
```

### **Step 4: Create Heroku App**
```bash
# Create a new Heroku app
heroku create atm-system-app

# Or let Heroku generate a random name
heroku create
```

### **Step 5: Deploy to Heroku**
```bash
# Push to Heroku
git push heroku main

# Or if you're on master branch
git push heroku master
```

### **Step 6: Open Your App**
```bash
# Open the deployed app in browser
heroku open

# Or get the URL
heroku info
```

## 🔧 Configuration Files

Your project already has the necessary files:

### **✅ requirements.txt**
```
Flask==2.3.3
Flask-CORS==4.0.0
gunicorn==21.2.0
requests==2.31.0
```

### **✅ Procfile**
```
web: gunicorn app:app
```

### **✅ app.py**
Your Flask app is ready for production.

## 🧪 Testing Your Deployment

### **Test Basic Functionality**
```bash
# Get balance
curl -X GET https://your-app-name.herokuapp.com/accounts/123456789/balance

# Deposit money
curl -X POST https://your-app-name.herokuapp.com/accounts/123456789/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 100.00}'

# Withdraw money
curl -X POST https://your-app-name.herokuapp.com/accounts/123456789/withdraw \
-H "Content-Type: application/json" \
-d '{"amount": 50.00}'
```

### **View Logs**
```bash
# View application logs
heroku logs --tail

# View recent logs
heroku logs
```

## 💰 Pricing

### **Free Tier (Discontinued)**
- No longer available for new accounts

### **Basic Dyno ($7/month)**
- Always running
- No sleep mode
- Perfect for small apps

### **Eco Dyno ($5/month)**
- Sleeps after 30 minutes of inactivity
- Wakes up on first request (may take 10-30 seconds)
- Good for development/testing

## 🔧 Useful Heroku Commands

```bash
# View app info
heroku info

# Open app in browser
heroku open

# View logs
heroku logs --tail

# Run commands on Heroku
heroku run python test_api.py

# Scale your app
heroku ps:scale web=1

# Check app status
heroku ps

# Restart app
heroku restart
```

## 🚨 Troubleshooting

### **Common Issues:**

1. **Build Fails**
   ```bash
   # Check build logs
   heroku logs --tail
   ```

2. **App Crashes**
   ```bash
   # Check crash logs
   heroku logs --tail
   
   # Restart the app
   heroku restart
   ```

3. **Port Issues**
   - Heroku automatically sets the PORT environment variable
   - Your app should use: `os.environ.get('PORT', 5000)`

### **Update Your App:**
```bash
# Make changes to your code
git add .
git commit -m "Update app"
git push heroku main
```

## 🎯 Quick Start Commands

```bash
# 1. Install Heroku CLI (from website)
# 2. Login
heroku login

# 3. Initialize git
git init
git add .
git commit -m "Initial commit"

# 4. Create and deploy
heroku create atm-system-app
git push heroku main

# 5. Open app
heroku open
```

## 📞 Need Help?

- **Heroku Documentation**: https://devcenter.heroku.com/
- **Heroku Support**: Available with paid plans
- **Community**: Heroku Community and Stack Overflow

## 🎉 Success!

Once deployed, your ATM system will be available at:
```
https://your-app-name.herokuapp.com
```

Your app will have:
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic scaling
- ✅ Built-in monitoring
