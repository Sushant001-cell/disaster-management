# Vercel Deployment Quick Setup

## Problem Solved
Fixed the "No flask entrypoint found" error by creating:
- ✅ `app.py` in root directory
- ✅ `vercel.json` configuration file
- ✅ `api/index.py` entry point
- ✅ `runtime.txt` for Python version
- ✅ `setup.py` for dependencies
- ✅ `pyproject.toml` for build configuration

## Deployment Steps

### 1. Prepare Your Repository
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### 2. Create PostgreSQL Database
For production, you need a PostgreSQL database (SQLite doesn't work on Vercel):

**Option A: Vercel Postgres**
- Go to Vercel Dashboard → Storage
- Create new Postgres database
- Copy the connection string

**Option B: External Database**
- AWS RDS, DigitalOcean, Railway, etc.
- Get your PostgreSQL connection string

### 3. Connect to Vercel

**Option A: Using Vercel CLI**
```bash
npm i -g vercel
vercel
# Follow prompts to connect GitHub repo
```

**Option B: Via Vercel Dashboard**
1. Go to https://vercel.com/import
2. Select your GitHub repository
3. Click "Import"

### 4. Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

Add these variables:
```
DATABASE_URL = postgresql://user:password@host:port/dbname
SECRET_KEY = your-strong-secret-key-here
FLASK_ENV = production
```

### 5. Deploy

After environment variables are set, click "Deploy" or push to main branch for auto-deploy.

### 6. Initialize Database

After first deployment, run database migrations:

```bash
vercel env pull  # Get environment variables locally
python -c "
import os
from backend.app import app, db
from backend.models import User, UserRole

os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL')

with app.app_context():
    db.create_all()
    
    # Create admin user
    admin = User.query.filter_by(email='admin@disaster.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@disaster.com',
            phone='9999999999',
            role=UserRole.ADMIN,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created')
"
```

## Testing After Deployment

1. **Health Check**
   ```
   https://your-project.vercel.app/api/health
   ```
   Should return: `{"status": "ok", "message": "Disaster Management System is running"}`

2. **Login**
   - Email: `admin@disaster.com`
   - Password: `admin123`

3. **Check Admin Dashboard**
   - Navigate to Dashboard after login
   - Should show all disaster reports

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Ensure `psycopg2-binary` is in `requirements.txt`

### Issue: Database connection error
**Solution**: Verify `DATABASE_URL` is correct and database is accessible

### Issue: Static files not loading
**Solution**: Frontend files are served from `frontend/` directory; verify paths in HTML

### Issue: CORS errors
**Solution**: CORS is enabled for all origins; for production, configure specific domains in `backend/app.py`

## Files Created/Modified

- ✅ `app.py` - Root entry point
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - API entry point
- ✅ `runtime.txt` - Python version
- ✅ `setup.py` - Package setup
- ✅ `pyproject.toml` - Build config
- ✅ `requirements.txt` - Added psycopg2
- ✅ `.env.production` - Production environment template
- ✅ `.vercelignore` - Files to ignore

## Next Steps

1. Push to GitHub
2. Connect to Vercel
3. Add environment variables
4. Deploy
5. Initialize database
6. Test endpoints

For more help, see `DEPLOYMENT.md`
