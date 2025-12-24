# Postman में Authentication कैसे Setup करें

## ⚠️ Important: GET Request में Body नहीं होती!

GET request के लिए authentication **Header** में होना चाहिए, Body में नहीं!

---

## Step-by-Step: Postman में Authentication Setup

### Step 1: पहले Login करें (Token लेने के लिए)

1. **New Request** बनाएं
2. **Method:** `POST`
3. **URL:** `http://127.0.0.1:8000/api/auth/login/`
4. **Body Tab:**
   - `raw` select करें
   - `JSON` select करें
   - Body में यह डालें:
   ```json
   {
       "email": "abc@gmail.com",
       "password": "abc@1234"
   }
   ```
5. **Send** button click करें

### Step 2: Response से Token Save करें

Login successful होने पर response में `tokens` object मिलेगा:
```json
{
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

**Token copy करें** (access token)

---

### Step 3: GET Request में Token Use करें

#### Method 1: Authorization Tab में (Recommended)

1. **GET Request** बनाएं
2. **URL:** `http://127.0.0.1:8000/api/auth/users/me/`
3. **Authorization Tab** पर click करें:
   - **Type:** `Bearer Token` select करें
   - **Token:** field में अपना `access_token` paste करें
4. **Body Tab:** 
   - **Body को EMPTY रखें** (GET request में body नहीं होती!)
   - या `none` select करें
5. **Send** button click करें

#### Method 2: Headers Tab में (Manual)

1. **GET Request** बनाएं
2. **URL:** `http://127.0.0.1:8000/api/auth/users/me/`
3. **Headers Tab** पर click करें:
   - **Key:** `Authorization`
   - **Value:** `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...` (पूरा token)
4. **Body Tab:** Empty रखें
5. **Send** button click करें

---

## ✅ Correct Setup Example

### GET /api/auth/users/me/ Request:

**Authorization Tab:**
```
Type: Bearer Token
Token: eyJ0eXAiOiJKV1QiLCJhbGc... (your access token)
```

**Headers Tab:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json
```

**Body Tab:**
```
none (empty - GET request में body नहीं होती!)
```

---

## ❌ Common Mistakes

### Mistake 1: GET Request में Body में Email/Password
```
❌ WRONG:
GET /api/auth/users/me/
Body: {
    "email": "abc@gmail.com",
    "password": "abc@1234"
}
```

### Mistake 2: Token Body में Send करना
```
❌ WRONG:
GET /api/auth/users/me/
Body: {
    "token": "eyJ0eXAi..."
}
```

### Mistake 3: Authorization Header Missing
```
❌ WRONG:
GET /api/auth/users/me/
(No Authorization header)
```

---

## ✅ Correct Way

```
✅ CORRECT:
GET /api/auth/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Body: (empty)
```

---

## 🔄 Complete Flow

### 1. Login (Token लें)
```
POST /api/auth/login/
Body: {
    "email": "abc@gmail.com",
    "password": "abc@1234"
}
Response: {
    "tokens": {
        "access": "eyJ0eXAi...",
        "refresh": "eyJ0eXAi..."
    }
}
```

### 2. Token Copy करें
- Response से `access` token copy करें

### 3. GET Request में Use करें
```
GET /api/auth/users/me/
Authorization: Bearer eyJ0eXAi... (paste token here)
Body: (empty)
```

---

## 🎯 Postman Environment Variables (Auto Setup)

### Step 1: Environment Create करें

1. Postman में **Environments** पर click करें
2. **"+"** button click करें
3. Environment name: `Pet Health API`
4. Variables add करें:
   - `base_url` = `http://127.0.0.1:8000`
   - `access_token` = (empty - automatically fill होगा)

### Step 2: Login Request में Token Auto-Save

**Login Request** के **Tests** tab में यह script add करें:

```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    if (jsonData.tokens) {
        pm.environment.set("access_token", jsonData.tokens.access);
        pm.environment.set("refresh_token", jsonData.tokens.refresh);
    }
}
```

### Step 3: GET Request में Auto-Use

**Authorization Tab:**
- Type: `Bearer Token`
- Token: `{{access_token}}` (environment variable)

अब हर request में automatically token use होगा!

---

## 📋 Quick Checklist

GET Request के लिए:
- [ ] पहले Login करके token लिया है?
- [ ] Authorization Tab में Bearer Token set किया है?
- [ ] Body Tab empty है? (GET में body नहीं होती)
- [ ] Token correct है? (expired तो नहीं?)

---

## 🔍 Troubleshooting

### Error: "401 Unauthorized"
**Problem:** Token missing या invalid  
**Solution:**
1. Login फिर से करें
2. नया token लें
3. Authorization header में correct token paste करें

### Error: "403 Forbidden"
**Problem:** Token valid है लेकिन permission नहीं है  
**Solution:** Admin role check करें

### Error: "404 Not Found"
**Problem:** URL गलत है  
**Solution:** URL check करें: `http://127.0.0.1:8000/api/auth/users/me/`

---

## 💡 Tips

1. **Token Expiry:** Access token 60 minutes के लिए valid है
2. **Refresh Token:** Expire होने पर refresh token use करें
3. **Environment Variables:** हमेशा use करें - आसान होता है
4. **Save Requests:** Collection में save करें ताकि बार-बार setup न करना पड़े

---

**Remember:** GET request = Header में Token, Body Empty! 🎯

