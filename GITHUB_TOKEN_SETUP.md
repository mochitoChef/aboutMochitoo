# 🔐 GitHub Personal Access Token Setup

## ❌ **Issue:** Password authentication no longer supported
GitHub has disabled password authentication for Git operations. You need a Personal Access Token.

## 🚀 **Quick Setup:**

### **Step 1: Create Personal Access Token**
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Token name:** `AboutMe Portfolio`
4. **Expiration:** `90 days` (or your preference)
5. **Scopes:** Check ✅ `repo` (Full control of private repositories)
6. Click **"Generate token"**
7. **COPY THE TOKEN** (you won't see it again!)

### **Step 2: Use Token to Push**
Replace `YOUR_TOKEN_HERE` with your actual token:

```bash
"C:\Program Files\Git\cmd\git.exe" remote set-url origin "https://MochitoChef:YOUR_TOKEN_HERE@github.com/mochitoChef/AboutMe.git"
"C:\Program Files\Git\cmd\git.exe" push -u origin main
```

### **Step 3: Alternative - Use GitHub CLI**
```bash
gh auth login
"C:\Program Files\Git\cmd\git.exe" push -u origin main
```

## 📁 **What Will Be Pushed:**
- ✅ Complete portfolio website
- ✅ Screenshot capture tools  
- ✅ AI conversion tools
- ✅ Documentation and launchers
- ✅ Custom favicon

## 🌐 **After Push:**
Your portfolio will be available at:
- **Repository:** https://github.com/mochitoChef/AboutMe
- **Local:** http://localhost:8080 (still running)

## 🎯 **Next Steps:**
1. Create the token (2 minutes)
2. Run the commands above
3. Enable GitHub Pages for live hosting
4. Share your portfolio!

The portfolio is ready to go live! 🚀

