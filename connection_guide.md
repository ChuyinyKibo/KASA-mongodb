# 🔗 MongoDB Connection Guide for Employers

## 🔐 Database Credentials
- **Username**: `kasa_admin`
- **Password**: `KasaChallenge2025!`
- **Host**: `localhost:27017`
- **Database**: `kasa_reservations`
- **Collection**: `reservations`
- **Connection String**: `mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations`

---

## 🛠️ Connection Methods

### **1. MongoDB Compass (Recommended for Employers)**
**Best for visual data exploration**

1. **Download**: https://www.mongodb.com/products/compass
2. **Connect**: Paste connection string: `mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations`
3. **Browse**: Navigate to `kasa_reservations` → `reservations` collection
4. **View**: All 10 documents with full details and aggregation capabilities

### **2. Python Scripts (Ready to Use)**
**Best for immediate verification**

```bash
# Quick verification
conda activate mongodb
python employer_demo.py

# Detailed connection test
python verify_connection.py

# Browse all data
python view_data.py
```

### **3. MongoDB Shell (Advanced Users)**
**Note**: Requires mongosh installation

```bash
# Connect (use single quotes to avoid bash issues)
mongosh 'mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations'

# Alternative: Connect then authenticate
mongosh localhost:27017
use kasa_reservations
db.auth("kasa_admin", "KasaChallenge2025!")
```

### **4. Live Web Interface**
**Best for immediate access**

- **Public URL**: https://85c8d5d220dd9bbf3b14aa9426a2a295.serveo.net
- **Features**: All 10 documents, aggregation results, responsive design
- **Access**: No setup required, works on any device

### **5. Custom Python Integration**
```python
from pymongo import MongoClient

# Connect to database
client = MongoClient("mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations")
collection = client.kasa_reservations.reservations

# View all documents
for doc in collection.find():
    print(f"Building: {doc['building']}, Code: {doc['reservation_code']}")

# Run aggregation pipeline
pipeline = [{
    "$project": {
        "_id": 0,
        "building_city": "$building",
        "confirmation_code": "$reservation_code",
        "booking_platform": "$booking_platform"
    }
}]

results = list(collection.aggregate(pipeline))
for i, doc in enumerate(results, 1):
    print(f"{i:2d}. {doc['building_city']:<12} {doc['confirmation_code']:<15} {doc['booking_platform']}")
```

---

## ⚡ Quick Verification

### **Instant Test Commands**
```bash
# Test connection (if mongosh installed)
mongosh 'mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations' --eval "db.reservations.countDocuments({})"

# Python verification (always works)
python -c "from pymongo import MongoClient; print('Documents:', MongoClient('mongodb://kasa_admin:KasaChallenge2025!@localhost:27017/kasa_reservations').kasa_reservations.reservations.count_documents({}))"
```

### **Expected Results**
- **Document Count**: 10
- **Building Codes**: AAA-1113, BBB-532, CCC-233, DDD-1102, EEE-437, FFF-2328, GGG-441, AAA-211, BBB-4403
- **Platforms**: source1, source2, source3

---

## 🔧 Troubleshooting

### **Connection Issues**
```bash
# Check MongoDB is running
docker ps | grep mongodb-kasa

# Start if stopped
docker start mongodb-kasa

# Check port accessibility
netstat -an | grep 27017
```

### **Authentication Problems**
- ✅ Username: `kasa_admin` (case-sensitive)
- ✅ Password: `KasaChallenge2025!` (exact characters)
- ✅ Database: `kasa_reservations` (not "admin")

### **Missing Data**
```bash
# Re-run setup if needed
python setup_mongodb_auth.py
```

---

## 📞 Support Scripts

**All scripts are ready to run from project directory:**

```bash
# 🔍 Connection verification
python verify_connection.py

# 👀 Browse all data
python view_data.py  

# 🎯 Employer demonstration
python employer_demo.py
```

**Status**: ✅ **All connection methods tested and verified**
