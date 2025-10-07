# Vercel Deployment Guide

This guide explains how to deploy RedCalibur to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: Obtain the following API keys:
   - Shodan API Key
   - Google Gemini API Key
   - VirusTotal API Key

## Deployment Steps

### 1. Connect Repository to Vercel

1. Go to your Vercel dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect the `vercel.json` configuration

### 2. Set Environment Variables

In your Vercel project settings, add these environment variables:

```
SHODAN_API_KEY=your_shodan_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
VERCEL=1
```

### 3. Deploy

Click "Deploy" - Vercel will:
1. Build the frontend (React + Vite)
2. Deploy the API as serverless functions
3. Set up routing between frontend and API

## Project Structure for Vercel

```
/
├── vercel.json              # Vercel configuration
├── api/
│   ├── index.py            # API entry point for Vercel
│   ├── app.py              # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── package.json        # Frontend dependencies
│   ├── vite.config.js      # Vite configuration
│   └── src/                # React source code
└── redcalibur/             # Core Python modules
```

## API Endpoints

After deployment, your API will be available at:
- `https://your-app.vercel.app/api/health` - Health check
- `https://your-app.vercel.app/api/domain` - Domain reconnaissance
- `https://your-app.vercel.app/api/scan` - Port scanning
- `https://your-app.vercel.app/api/username` - Username lookup
- `https://your-app.vercel.app/api/urlscan` - URL scanning

## Key Changes for Serverless Deployment

1. **Logging**: Changed to console-only logging (no file logging in serverless)
2. **CORS**: Configured for production domains
3. **Error Handling**: Improved for serverless environment
4. **Dependencies**: Removed uvicorn (not needed in Vercel)
5. **File System**: Removed file system dependencies

## Troubleshooting

### API Not Working
1. Check environment variables are set correctly
2. Verify API keys are valid
3. Check Vercel function logs

### CORS Issues
1. Ensure your frontend domain is in the allowed origins
2. Check that VERCEL environment variable is set

### Build Failures
1. Check that all dependencies are in requirements.txt
2. Verify Python version compatibility
3. Check Vercel build logs

## Local Development

For local development:

```bash
# Backend
cd api
pip install -r requirements.txt
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

Create `.env` files based on `.env.example` files for local configuration.