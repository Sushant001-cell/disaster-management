# Deployment Guide

## Vercel Deployment

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository of this project
- PostgreSQL database (recommended for production)

### Step 1: Prepare Database

For Vercel (serverless), you should use **PostgreSQL** instead of SQLite:

1. Create a PostgreSQL database (using Vercel Postgres, AWS RDS, etc.)
2. Get your database connection string in format:
   ```
   postgresql://user:password@host:port/database_name
   ```

### Step 2: Configure Environment Variables in Vercel

1. Go to your Vercel project settings
2. Add the following environment variables:

```
DATABASE_URL=postgresql://user:password@host:port/database_name
SECRET_KEY=your-secure-secret-key-change-this
FLASK_ENV=production
```

### Step 3: Deploy to Vercel

**Option 1: Using Vercel CLI**
```bash
npm install -g vercel
vercel
```

**Option 2: Using GitHub Integration**
1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Vercel will auto-deploy on push

### Step 4: Test the Deployment

After deployment, visit your Vercel project URL:
- Check `/api/health` endpoint
- Login with admin credentials:
  - Email: `admin@disaster.com`
  - Password: `admin123`

## Local Development

### Requirements
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
python backend/app.py
```

Access at: `http://localhost:8000`

## Database Migrations (Production)

For production PostgreSQL database initialization:

```bash
python -c "from backend.app import app, db; 
with app.app_context(): 
    db.create_all()"
```

## Important Notes

1. **Database**: SQLite works for local development but not on Vercel. Use PostgreSQL for production.
2. **Static Files**: Frontend files are served from `frontend/` directory
3. **API Routes**: All backend routes are under `/api/` prefix
4. **CORS**: Enabled for all origins in development; configure properly for production

## Troubleshooting

### Error: No flask entrypoint found
- Ensure `app.py` or `api/index.py` exists in root or api folder
- Check `vercel.json` configuration

### Database Connection Error
- Verify `DATABASE_URL` environment variable is set correctly
- Ensure your database is accessible from Vercel's servers

### Static Files Not Loading
- Check that `frontend/` directory is properly configured in `vercel.json`
- Verify MIME types are set correctly

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Database connection string (PostgreSQL) |
| `SECRET_KEY` | Yes | Flask secret key for sessions |
| `FLASK_ENV` | No | Set to `production` for deployment |
| `MAIL_SERVER` | No | Email server for notifications |
| `MAIL_USERNAME` | No | Email account username |
| `MAIL_PASSWORD` | No | Email account password |

## Production Checklist

- [ ] Environment variables configured in Vercel
- [ ] PostgreSQL database created and accessible
- [ ] SECRET_KEY is strong and unique
- [ ] CORS origins properly configured
- [ ] Database migrations run successfully
- [ ] Static files serving correctly
- [ ] API health check passing
