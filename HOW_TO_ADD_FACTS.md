# 📝 HOW TO ADD NEW FACTS TO ARI

## 🎯 **Main File to Edit:**
`learned_facts_expanded.json`

## 📖 **Step-by-Step Instructions:**

### **Method 1: Manual Addition (Simple)**

1. **Open** `learned_facts_expanded.json` in any text editor
2. **Go to the very end** of the file (find the closing `]`)
3. **Before the closing `]`**, add your new fact:

```json
  {
    "question": [
      "what is your new topic",
      "what is your new topic?", 
      "tell me about your new topic",
      "explain your new topic",
      "your new topic definition"
    ],
    "answer": "Your comprehensive answer about the new topic goes here."
  }
```

4. **Make sure** to add a comma after the previous fact
5. **Save** the file
6. **Restart ARI**

### **Example: Adding "Blockchain" Knowledge**

Find the end of the file and add:

```json
  {
    "question": [
      "what is blockchain",
      "what is blockchain?",
      "tell me about blockchain", 
      "explain blockchain",
      "blockchain definition",
      "define blockchain",
      "how does blockchain work"
    ],
    "answer": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, which are linked and secured using cryptography. It enables secure, transparent, and decentralized transactions without requiring a central authority."
  }
```

### **Method 2: Using Enhancement Tools (Advanced)**

1. Add a basic fact with simple questions
2. Run `enhance_questions_advanced.py` to auto-generate 40+ question variations
3. Restart ARI

## ✅ **Result:**
- ARI will **immediately recognize** all question variations
- **No training** or manual updates needed
- Works with **exact and fuzzy matching**

## 🧪 **Test Your New Facts:**
Run `test_enhanced_matching.py` to verify your new facts work correctly.

## 📁 **File Structure:**
```
learned_facts_expanded.json  ← ADD NEW FACTS HERE
├── add_fact.py             ← Helper script (optional)
├── enhance_questions_advanced.py ← Question generator (optional)  
└── test_enhanced_matching.py     ← Test your changes (optional)
```

## 🎯 **Key Points:**
- Facts are loaded **fresh each time** ARI starts
- Questions become available **immediately** after restart
- **No programming knowledge** required for basic fact addition
- JSON format must be **valid** (watch commas and brackets)
