# Vercel Deployment Guide

## Issues Fixed

### 1. Backend API Structure
- ✅ Created proper `requirements.txt` in `backend/api/` directory
- ✅ Fixed import issues in `index.py`
- ✅ Updated Vercel handler function for serverless compatibility
- ✅ Added proper error handling for imports

### 2. Vercel Configuration
- ✅ Updated `vercel.json` with proper build configuration
- ✅ Added function timeout and size limits
- ✅ Updated `.vercelignore` to exclude unnecessary files

### 3. File Structure
```
E-commerceSalesChatBot/
├── vercel.json                 # Vercel deployment configuration
├── .vercelignore              # Files to exclude from deployment
├── requirements.txt           # Root requirements (minimal)
├── frontend/                  # React frontend
│   ├── package.json
│   └── ...
└── backend/
    └── api/                   # Vercel serverless functions
        ├── index.py           # Main API entry point
        ├── mock_data.py       # Product data
        └── requirements.txt   # Python dependencies
```

## Deployment Steps

### 1. Prerequisites
- Vercel CLI installed: `npm install -g vercel`
- Git repository connected to Vercel

### 2. Deploy to Vercel
```bash
# From the project root directory
vercel

# Or for production deployment
vercel --prod
```

### 3. Environment Variables (if needed)
If you need to add environment variables:
```bash
vercel env add VARIABLE_NAME
```

### 4. Test Deployment
After deployment, test these endpoints:
- `https://your-app.vercel.app/` - Home page
- `https://your-app.vercel.app/api/products` - Products API
- `https://your-app.vercel.app/api/products/categories` - Categories API
- `https://your-app.vercel.app/api/auth/login` - Login API
- `https://your-app.vercel.app/api/chat/start` - Chat API

## Common Issues and Solutions

### Issue 1: Import Errors
**Problem**: `ImportError: No module named 'mock_data'`
**Solution**: ✅ Fixed by placing `mock_data.py` in the same directory as `index.py`

### Issue 2: Missing Dependencies
**Problem**: `ModuleNotFoundError: No module named 'flask'`
**Solution**: ✅ Fixed by creating `requirements.txt` in `backend/api/` directory

### Issue 3: Serverless Function Timeout
**Problem**: Function times out during execution
**Solution**: ✅ Added timeout configuration in `vercel.json`

### Issue 4: Large Bundle Size
**Problem**: Deployment fails due to large bundle size
**Solution**: ✅ Added `.vercelignore` to exclude unnecessary files

## API Endpoints

### Products
- `GET /api/products` - Get all products with pagination and filtering
- `GET /api/products/categories` - Get all product categories

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile

### Chat
- `POST /api/chat/start` - Start chat session
- `POST /api/chat/message` - Send chat message

## Testing

### Local Testing
```bash
# Test the API locally
cd backend/api
python index.py

# In another terminal, test endpoints
python ../../test_vercel_api.py
```

### Production Testing
Update the `test_vercel_api.py` file with your Vercel URL and run:
```bash
python test_vercel_api.py
```

## Troubleshooting

### Check Vercel Logs
```bash
vercel logs
```

### Check Function Status
```bash
vercel ls
```

### Redeploy
```bash
vercel --prod
```

## Next Steps
1. Deploy to Vercel using `vercel --prod`
2. Test all API endpoints
3. Update frontend API URLs to point to your Vercel deployment
4. Configure custom domain (optional)
