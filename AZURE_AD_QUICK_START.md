# Azure AD Authentication - Quick Start Guide

## Prerequisites Checklist
- [ ] Azure AD tenant with admin access
- [ ] The Grid code deployed locally and/or on Azure

## Step 1: Azure AD App Registration (5 minutes)

1. **Azure Portal** → **Azure Active Directory** → **App registrations** → **+ New registration**
2. **Name**: `The Grid`
3. **Redirect URI**:
   - Platform: **Web**
   - URI: `http://localhost:8000/oidc/callback/`
4. Click **Register**

## Step 2: Configure Authentication (3 minutes)

1. Go to **Authentication** → **+ Add a platform** → **Web**
2. Add redirect URIs:
   - `http://localhost:8000/oidc/callback/`
   - `https://the-grid-v2.azurewebsites.net/oidc/callback/`
3. Under **Implicit grant**: Check **ID tokens**
4. Click **Save**

## Step 3: Create Client Secret (2 minutes)

1. Go to **Certificates & secrets** → **+ New client secret**
2. **Description**: `The Grid Production`
3. **Expires**: 12 or 24 months
4. Click **Add**
5. **Copy the secret VALUE immediately** (won't show again!)

## Step 4: Note Configuration Values (1 minute)

From the **Overview** page, copy:
- **Application (client) ID**: `OIDC_RP_CLIENT_ID`
- **Directory (tenant) ID**: `OIDC_TENANT_ID`
- **Client secret value** (from Step 3): `OIDC_RP_CLIENT_SECRET`

## Step 5: Configure Local Environment (2 minutes)

Create/update `.env` file in project root:

```bash
OIDC_RP_CLIENT_ID=<paste-client-id-here>
OIDC_RP_CLIENT_SECRET=<paste-secret-value-here>
OIDC_TENANT_ID=<paste-tenant-id-here>
CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

## Step 6: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 7: Test Locally (2 minutes)

```bash
python manage.py migrate
python manage.py runserver
```

Navigate to `http://localhost:8000` and click **Sign in with Microsoft**.

## Step 8: Configure Azure App Service (3 minutes)

1. **Azure Portal** → Your **App Service** → **Configuration**
2. Add these **Application settings**:
   - `OIDC_RP_CLIENT_ID` = Your client ID
   - `OIDC_RP_CLIENT_SECRET` = Your secret value
   - `OIDC_TENANT_ID` = Your tenant ID
   - `CSRF_TRUSTED_ORIGINS` = `https://the-grid-v2.azurewebsites.net`
3. Click **Save** → **Continue** (to restart app)

## Step 9: Deploy & Test Production (5 minutes)

1. Deploy your updated code to Azure App Service
2. Navigate to `https://the-grid-v2.azurewebsites.net`
3. Click **Sign in with Microsoft**
4. Verify authentication works!

---

## Troubleshooting

### "Redirect URI does not match"
→ Check exact URI in Azure AD matches Django's endpoint (include trailing slash!)

### "CSRF verification failed"
→ Verify `CSRF_TRUSTED_ORIGINS` is set in environment

### "Invalid client secret"
→ Check secret value and expiration date in Azure AD

---

## Key URLs

| Environment | Sign In URL | Callback URL |
|-------------|------------|--------------|
| Local | http://localhost:8000/oidc/authenticate/ | http://localhost:8000/oidc/callback/ |
| Production | https://the-grid-v2.azurewebsites.net/oidc/authenticate/ | https://the-grid-v2.azurewebsites.net/oidc/callback/ |

---

## Full Documentation

See `docs/AZURE_AD_SETUP.md` for complete setup guide, troubleshooting, and advanced configuration.

---

**Total Setup Time**: ~20 minutes
