# Club77 Check-In App - Domain Migration Complete ✅

**Date:** 2025-05-28  
**App:** Club77 Check-In System (Tailwind)  
**Port:** 3005  
**Migration:** club77.projekt-ai.net → guestlist.club77.com.au

## 🎯 **Migration Summary**

Successfully migrated the Club77 Check-In app from the temporary projekt-ai.net subdomain to the official club77.com.au domain structure.

### **Before:**
- **URL:** https://club77.projekt-ai.net
- **Domain:** Temporary subdomain on projekt-ai.net
- **SSL:** Let's Encrypt certificate

### **After:**
- **URL:** https://guestlist.club77.com.au ✅
- **Domain:** Official club77.com.au subdomain
- **SSL:** Let's Encrypt certificate (existing, redeployed)

## 🔧 **Technical Changes Made**

### 1. **DNS Configuration**
- ✅ DNS record added to Cloudflare for club77.com.au
- ✅ `guestlist` subdomain pointing to 192.168.1.107

### 2. **Nginx Configuration**
- ✅ Created new config: `/etc/nginx/sites-available/guestlist.club77.com.au`
- ✅ Enabled new site: `ln -sf /etc/nginx/sites-available/guestlist.club77.com.au /etc/nginx/sites-enabled/`
- ✅ Disabled old site: `rm /etc/nginx/sites-enabled/club77.projekt-ai.net`
- ✅ Configuration tested and reloaded

### 3. **SSL Certificate**
- ✅ Existing certificate found and redeployed
- ✅ HTTPS working correctly with automatic HTTP→HTTPS redirect
- ✅ Certificate managed by Certbot

### 4. **Application Configuration**
- ✅ App continues running on port 3005
- ✅ No application code changes required
- ✅ All functionality preserved

## 🧪 **Testing Results**

```bash
curl -I https://guestlist.club77.com.au
# HTTP/2 302 
# server: nginx
# location: /login
# ✅ Redirects to login as expected
```

### **Functionality Verified:**
- ✅ HTTPS access working
- ✅ Login page loads correctly
- ✅ SSL certificate valid
- ✅ Automatic HTTP→HTTPS redirect
- ✅ App responds correctly

## 📋 **Configuration Files**

### **Nginx Configuration:**
```nginx
# /etc/nginx/sites-available/guestlist.club77.com.au
server {
    server_name guestlist.club77.com.au;
    
    location / {
        proxy_pass http://localhost:3005;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/guestlist.club77.com.au/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/guestlist.club77.com.au/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = guestlist.club77.com.au) {
        return 301 https://$host$request_uri;
    }
    
    listen 80;
    server_name guestlist.club77.com.au;
    return 404;
}
```

## 📝 **Documentation Updates**

### **Updated Files:**
- ✅ `/root/homelab-docs/PORT-TRACKER.md` - Updated domain reference
- ✅ Created this migration summary document

### **PORT-TRACKER.md Entry:**
```
| 3005 | Club77 Check-In (Tailwind) | Beautiful staff dashboard with Mailchimp integration | Docker container (Category C) ✅ PRODUCTION - https://guestlist.club77.com.au |
```

## 🎉 **Migration Complete**

The Club77 Check-In app is now successfully running on its official domain:

**🌐 https://guestlist.club77.com.au**

### **Benefits:**
- ✅ **Professional branding** - Uses official club77.com.au domain
- ✅ **Intuitive URL** - `guestlist.club77.com.au` clearly indicates purpose
- ✅ **SSL secured** - Full HTTPS with valid certificate
- ✅ **Zero downtime** - Migration completed without service interruption
- ✅ **Maintained functionality** - All features working as before

### **Next Steps:**
- Update any bookmarks or saved links to use the new domain
- Inform staff of the new URL for accessing the guest list system
- Consider updating any documentation that references the old domain

**The Club77 Check-In app is now live on its permanent, professional domain! 🚀** 