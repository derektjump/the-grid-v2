# Azure AD / Entra ID Authentication Setup Guide

This document provides step-by-step instructions for configuring Azure AD (Microsoft Entra ID) authentication for The Grid using OpenID Connect (OIDC).

## Overview

The Grid uses `mozilla-django-oidc` library to authenticate users via Microsoft Azure AD / Entra ID. Users will click "Sign in with Microsoft" and be redirected to Microsoft's login page. After successful authentication, they'll be redirected back to The Grid.

---

## Prerequisites

- An Azure AD (Entra ID) tenant
- Admin access to Azure Portal
- The Grid deployed locally and/or on Azure App Service

---

## Step 1: Register Application in Azure AD

### 1.1 Navigate to Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** (or **Microsoft Entra ID**)
3. Click **App registrations** in the left sidebar
4. Click **+ New registration**

### 1.2 Configure App Registration

**Application Details:**
- **Name**: `The Grid` (or your preferred name)
- **Supported account types**:
  - Choose "Accounts in this organizational directory only" for single-tenant (recommended)
  - OR "Accounts in any organizational directory" for multi-tenant
- **Redirect URI**:
  - Platform: **Web**
  - For local development, add: `http://localhost:8000/oidc/callback/`
  - You'll add production URI after deployment

Click **Register**

### 1.3 Configure Authentication

After registration, you'll be on the app's Overview page.

1. Click **Authentication** in the left sidebar
2. Under **Redirect URIs**, click **+ Add a platform** → **Web**
3. Add both local and production URIs:
   - `http://localhost:8000/oidc/callback/`
   - `https://the-grid-v2.azurewebsites.net/oidc/callback/`
   - (Replace `the-grid-v2` with your actual Azure App Service name)
4. Under **Implicit grant and hybrid flows**:
   - Check **ID tokens** (used for user sign-in)
5. Under **Supported account types**: Verify it matches your choice from Step 1.2
6. Click **Save**

### 1.4 Create Client Secret

1. Click **Certificates & secrets** in the left sidebar
2. Click **+ New client secret**
3. **Description**: `The Grid Production Secret` (or your preferred description)
4. **Expires**: Choose expiration (recommend 12 or 24 months)
5. Click **Add**
6. **IMPORTANT**: Copy the **Value** immediately - it won't be shown again!
   - This is your `OIDC_RP_CLIENT_SECRET`

### 1.5 Configure API Permissions

1. Click **API permissions** in the left sidebar
2. Verify the following permissions are present (should be added by default):
   - **Microsoft Graph** → **openid** (Sign in and read user profile)
   - **Microsoft Graph** → **profile** (View users' basic profile)
   - **Microsoft Graph** → **email** (View users' email address)
3. If not present, click **+ Add a permission** → **Microsoft Graph** → **Delegated permissions**
4. Add the permissions above
5. Click **Grant admin consent** (if you have admin rights)

### 1.6 Collect Required Information

From the **Overview** page, copy the following values:

- **Application (client) ID**: This is your `OIDC_RP_CLIENT_ID`
- **Directory (tenant) ID**: This is your `OIDC_TENANT_ID`

You should now have three values:
1. `OIDC_RP_CLIENT_ID` (from Overview → Application ID)
2. `OIDC_RP_CLIENT_SECRET` (from Certificates & secrets → Client secret value)
3. `OIDC_TENANT_ID` (from Overview → Directory ID)

---

## Step 2: Configure Local Development Environment

### 2.1 Create or Update .env File

Create a `.env` file in your project root (if it doesn't exist):

```bash
# Azure AD Authentication
OIDC_RP_CLIENT_ID=12345678-1234-1234-1234-123456789012
OIDC_RP_CLIENT_SECRET=your-secret-value-from-step-1.4
OIDC_TENANT_ID=87654321-4321-4321-4321-210987654321

# Django Settings
DJANGO_SETTINGS_MODULE=the_grid.settings.local
```

Replace the example GUIDs with your actual values from Step 1.6.

### 2.2 Load Environment Variables

The project uses `python-dotenv` to automatically load `.env` files. Ensure your `manage.py` and `wsgi.py` load the environment variables.

If using a different method (like system environment variables), set them accordingly.

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `mozilla-django-oidc>=4.0.0` and other dependencies.

### 2.4 Run Migrations

```bash
python manage.py migrate
```

### 2.5 Test Locally

```bash
python manage.py runserver
```

Navigate to `http://localhost:8000` and click **Sign in with Microsoft**. You should be redirected to Microsoft's login page.

---

## Step 3: Configure Production (Azure App Service)

### 3.1 Add Redirect URI to Azure AD

If you haven't already added the production redirect URI:

1. Go to Azure Portal → Azure AD → App registrations → Your app
2. Click **Authentication**
3. Under **Redirect URIs**, add:
   - `https://the-grid-v2.azurewebsites.net/oidc/callback/`
   - (Replace with your actual Azure App Service URL)
4. Click **Save**

### 3.2 Configure Azure App Service Environment Variables

1. Go to Azure Portal
2. Navigate to your **App Service** (The Grid)
3. Click **Configuration** (under Settings in left sidebar)
4. Click **+ New application setting** for each of the following:

| Name | Value | Description |
|------|-------|-------------|
| `OIDC_RP_CLIENT_ID` | Your Application (client) ID | From Azure AD app registration |
| `OIDC_RP_CLIENT_SECRET` | Your client secret value | From Azure AD Certificates & secrets |
| `OIDC_TENANT_ID` | Your Directory (tenant) ID | From Azure AD app registration |
| `CSRF_TRUSTED_ORIGINS` | `https://the-grid-v2.azurewebsites.net` | Required for OIDC callback security |
| `DJANGO_SETTINGS_MODULE` | `the_grid.settings.production` | Ensure production settings are used |

5. Click **Save** (at the top)
6. Click **Continue** to restart the app

### 3.3 Deploy Updated Code

Ensure your latest code (with OIDC integration) is deployed to Azure App Service.

If using GitHub Actions or Azure DevOps, push your changes and wait for deployment to complete.

### 3.4 Test Production

1. Navigate to `https://the-grid-v2.azurewebsites.net`
2. Click **Sign in with Microsoft**
3. You should be redirected to Microsoft's login page
4. After authentication, you should be redirected back to The Grid

---

## Step 4: Troubleshooting

### Common Issues

#### 1. "AADSTS50011: The redirect URI does not match"

**Solution**: Verify that the redirect URI in Azure AD exactly matches the one Django is using:
- Local: `http://localhost:8000/oidc/callback/`
- Production: `https://your-app-name.azurewebsites.net/oidc/callback/`

Note: URLs are case-sensitive and must include trailing slash.

#### 2. "CSRF verification failed"

**Solution**: Ensure `CSRF_TRUSTED_ORIGINS` is set correctly in Azure App Service Configuration:
- Value should be: `https://the-grid-v2.azurewebsites.net` (no trailing slash, https required)

#### 3. "Invalid client secret"

**Solution**:
- Verify `OIDC_RP_CLIENT_SECRET` is set correctly in Azure App Service Configuration
- Client secrets expire - check expiration in Azure AD → Certificates & secrets
- If expired, create a new secret and update the App Service configuration

#### 4. User is authenticated but shows "Guest User"

**Solution**: This means authentication is working but user profile isn't being synced. Check:
- API permissions in Azure AD include `openid`, `profile`, and `email`
- Admin consent has been granted for these permissions
- Check Django logs for errors during user profile retrieval

#### 5. "Connection refused" or "Cannot connect to Microsoft"

**Solution**:
- Verify outbound network connectivity from Azure App Service
- Check if any firewall rules are blocking HTTPS traffic to `login.microsoftonline.com`
- Verify DNS resolution is working

#### 6. Login works but user is immediately logged out

**Solution**:
- Check session configuration in Django settings
- Verify `SESSION_COOKIE_SECURE = True` in production (but False in local)
- Check if Azure App Service is properly handling HTTPS

---

## Step 5: Security Best Practices

### Protect Client Secrets

- **Never commit secrets to version control**
- Store secrets in Azure App Service Configuration (production)
- Store secrets in `.env` file locally (add `.env` to `.gitignore`)
- Rotate client secrets regularly (recommended: every 6-12 months)

### Monitor Token Expiration

- Azure AD tokens typically expire after 1 hour
- The Grid automatically refreshes tokens every 15 minutes (configured via `OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS`)
- Users may need to re-authenticate after extended idle periods

### Restrict User Access

To limit which users can access The Grid:

1. In Azure AD → App registrations → Your app
2. Click **Overview** → **Managed application in local directory**
3. Click **Properties**
4. Set **User assignment required?** to **Yes**
5. Click **Save**
6. Go to **Users and groups** to assign specific users/groups

### Enable Logging

Monitor authentication attempts and issues:

1. In Azure AD → App registrations → Your app
2. Click **Monitoring** → **Sign-in logs**
3. Review successful and failed authentication attempts

---

## Step 6: Advanced Configuration

### Multi-Tenant Applications

If you want users from any Azure AD tenant to sign in:

1. In Azure AD → App registrations → Your app → **Authentication**
2. Under **Supported account types**, select:
   - "Accounts in any organizational directory (Any Azure AD directory - Multitenant)"
3. In your `.env` or Azure App Service Configuration:
   - Set `OIDC_TENANT_ID=common` (instead of specific tenant ID)

### Custom Claims

To access additional user information:

1. Configure additional API permissions in Azure AD
2. Create a custom OIDC backend that extends `OIDCAuthenticationBackend`
3. Override the `create_user` and `update_user` methods to handle custom claims

---

## Endpoints Summary

The Grid provides these authentication endpoints:

| Endpoint | Purpose | Public |
|----------|---------|--------|
| `/oidc/authenticate/` | Initiates login with Azure AD | Yes |
| `/oidc/callback/` | Azure AD redirects here after authentication | No (callback only) |
| `/oidc/logout/` | Logs out user and clears session | Yes |
| `/health/` | Health check (doesn't require auth) | Yes |

---

## Reference: Environment Variables

Complete list of environment variables for Azure AD authentication:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OIDC_RP_CLIENT_ID` | Yes | - | Application (client) ID from Azure AD |
| `OIDC_RP_CLIENT_SECRET` | Yes | - | Client secret from Azure AD |
| `OIDC_TENANT_ID` | Yes | `common` | Directory (tenant) ID or 'common' for multi-tenant |
| `OIDC_RP_SIGN_ALGO` | No | `RS256` | Signing algorithm (Azure AD uses RS256) |
| `CSRF_TRUSTED_ORIGINS` | Yes (prod) | - | Comma-separated list of trusted origins |

---

## Support & Resources

### Microsoft Documentation
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [OpenID Connect on Azure AD](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc)

### Library Documentation
- [mozilla-django-oidc](https://mozilla-django-oidc.readthedocs.io/)

### The Grid Documentation
- See `docs/PLATFORM_OVERVIEW.md` for overall architecture
- See `the_grid/settings/base.py` for OIDC configuration details

---

## Changelog

### 2025-11-23
- Initial Azure AD / OIDC integration
- Added mozilla-django-oidc library
- Configured authentication endpoints
- Updated templates with Sign in/Sign out functionality
