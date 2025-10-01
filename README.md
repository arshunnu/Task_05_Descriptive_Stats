# 🧠 Research Task 05 — LLM vs Python Stats Check

**Dataset:** Syracuse University Women’s Lacrosse (2025 Season)  

I asked the model a few basic questions:

1. How many games did the team play?
2. What was the overall record?
3. What was the home record?
4. What was the away record?
5. What was the avg goal count for?
6. What was the avg goal count against?
7. What was the avg goal count difference?

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
