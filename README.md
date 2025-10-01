# 🧠 Research Task 05 — LLM vs Python Stats Check

**Dataset:** Syracuse University Women’s Lacrosse (2025 Season)  
**Goal:** See how well ChatGPT can read and analyze real game data, then verify it with Python.

---

## 🎯 What This Is
This project compares what **ChatGPT** says about a small sports dataset with what **Python** actually calculates.

I asked the model 3 basic questions:
1. How many games were played, and what’s the record (Home/Away)?
2. Should the team focus more on offense or defense to flip close losses?
3. Which opponent could they beat next time with a small change?

Everything’s checked against ground truth using a Python script.

---

## 🧩 Tools I Used
- **Python** (pandas + openpyxl)  
- **ChatGPT-4o** for the answers  
- **Excel** for easy viewing  

---

## 🧮 What Python Found
| Metric | Value |
|:--------|:------|
| Games Played | 15 |
| Record | 9–6 |
| Home | 6–1 |
| Away | 3–3 |
| Avg Goals For | 13.73 |
| Avg Goals Against | 10.40 |
| Avg Goal Diff | +3.33 |

📊 All details are in **`ground_truth_report.xlsx`** (Summary, Wins, Losses, Highlights).

---

## 🤖 What ChatGPT Said
The first try was off — it counted **10 games** and messed up averages.  
After clarifying the columns, the second run matched perfectly ✅  

See [`docs/LLM_Discrepancy_Report.md`](./docs/LLM_Discrepancy_Report.md) for that comparison.

---

## ⚙️ How To Run
Just run:
```bash
python stats_verification.py
