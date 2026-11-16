# 🚀 Deployment Guide for netguard.piupiu.kz

**Stack Name:** `netguard-demo`  
**Target Host:** `netguard.piupiu.kz`  
**Container Port:** `8000`  
**Network:** `platform-net` (external Traefik reverse proxy)  

---

## 🛠️ Quick Deployment Commands

1. **Clone repository onto the server:**
   ```bash
   git clone https://github.com/Mad03633/NetGuard.git ~/tenants/netguard-demo
   cd ~/tenants/netguard-demo
   ```

2. **Ensure `platform-net` Docker network exists:**
   ```bash
   docker network create platform-net || true
   ```

3. **Deploy stack using Docker Compose:**
   ```bash
   docker compose up -d --build
   ```

4. **Verify container health & Traefik router status:**
   ```bash
   docker compose ps
   docker compose logs -f netguard-demo
   ```

5. **Test domain in browser:**
   Open `https://netguard.piupiu.kz`
