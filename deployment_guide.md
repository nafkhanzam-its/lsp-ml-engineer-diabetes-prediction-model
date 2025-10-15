# Deployment Guide - Diabetes Risk Prediction System

This guide provides instructions for deploying the Diabetes Risk Prediction System to various cloud platforms.

## 🚀 Quick Local Testing

### Using Flask Development Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Using Docker
```bash
# Build the Docker image
docker build -t diabetes-predictor .

# Run the container
docker run -p 5000:5000 diabetes-predictor
```

### Using Docker Compose
```bash
# Start all services (app + nginx)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Platform Deployments

### 1. Railway (Recommended for beginners)

**Steps:**
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect `railway.json` and deploy
4. Your app will be available at `https://your-app.railway.app`

**Configuration:**
- Uses `railway.json` for build configuration
- Automatic HTTPS and custom domains available
- Built-in monitoring and logs

### 2. Render

**Steps:**
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Render will detect `render.yaml` and deploy
4. Free tier available with some limitations

**Features:**
- Free SSL certificates
- Automatic deployments from Git
- Built-in monitoring

### 3. Vercel

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in project directory
3. Follow the prompts
4. Uses `vercel.json` for configuration

**Notes:**
- Optimized for serverless functions
- Excellent for static content delivery
- May have cold start delays

### 4. Heroku

**Steps:**
1. Install Heroku CLI
2. Create new app: `heroku create your-app-name`
3. Deploy: `git push heroku main`
4. Uses `Procfile` and `runtime.txt`

**Commands:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create diabetes-predictor-app

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open app
heroku open
```

### 5. DigitalOcean App Platform

**Steps:**
1. Create account at DigitalOcean
2. Use App Platform
3. Connect your GitHub repository
4. Configure using the web interface

### 6. AWS (Advanced)

**Using Elastic Beanstalk:**
1. Install AWS CLI and EB CLI
2. Run `eb init` and `eb create`
3. Uses `requirements.txt` automatically

**Using ECS/Fargate:**
1. Build and push Docker image to ECR
2. Create ECS task definition
3. Deploy to Fargate cluster

### 7. Google Cloud Platform

**Using Cloud Run:**
```bash
# Build and deploy
gcloud run deploy diabetes-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 8. Azure

**Using Container Instances:**
1. Build Docker image
2. Push to Azure Container Registry
3. Deploy to Container Instances

## 🔧 Environment Variables

Set these environment variables in your deployment platform:

```
FLASK_ENV=production
PYTHONPATH=/app
```

## 🔒 Security Considerations

### For Production Deployments:

1. **Enable HTTPS:**
   - Most platforms provide free SSL certificates
   - Update nginx.conf for SSL termination if using custom setup

2. **Environment Variables:**
   - Never commit sensitive data to version control
   - Use platform-specific environment variable management

3. **Rate Limiting:**
   - Nginx configuration includes rate limiting
   - Consider using CloudFlare for additional protection

4. **CORS Configuration:**
   - Update Flask app if serving API to different domains

5. **Health Checks:**
   - All configurations include `/health` endpoint
   - Monitor application health regularly

## 📊 Monitoring and Logging

### Built-in Monitoring:
- Health check endpoint: `/health`
- Application metrics via platform dashboards

### Custom Monitoring:
```python
# Add to app.py for custom metrics
import logging
logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Railway
      uses: railway-app/github-action@v1
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 📝 Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] All forms submit correctly
- [ ] Predictions are working
- [ ] Health check endpoint responds
- [ ] SSL certificate is valid
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring alerts set up
- [ ] Error tracking configured

## 🆘 Troubleshooting

### Common Issues:

1. **Model Files Missing:**
   - Ensure `.pkl` files are included in deployment
   - Check file paths in `app.py`

2. **Memory Issues:**
   - Increase worker memory limits
   - Consider using fewer workers

3. **Timeout Errors:**
   - Increase timeout settings in deployment config
   - Optimize model loading

4. **Static Files Not Loading:**
   - Check static file paths
   - Ensure nginx configuration is correct

### Debug Commands:
```bash
# Check application logs
docker logs diabetes-predictor-app

# Check nginx logs
docker logs diabetes-predictor-nginx

# Test health endpoint
curl http://localhost:5000/health
```

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Test locally first
4. Check firewall and security group settings

## 🔗 Platform-Specific Documentation

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Heroku Docs](https://devcenter.heroku.com/)
- [AWS Docs](https://docs.aws.amazon.com/)
- [GCP Docs](https://cloud.google.com/docs)
- [Azure Docs](https://docs.microsoft.com/azure/)

---

**Note:** Choose the platform that best fits your needs, budget, and technical requirements. Railway and Render are excellent for beginners, while AWS/GCP/Azure offer more advanced features for enterprise deployments.