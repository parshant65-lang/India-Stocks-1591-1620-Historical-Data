# India-Stocks-1591-1620-Historical-Data

Institutional Historical 1-Minute Market Data Archive for **India Equities (Constituents 1591 to 1620)** with automated daily cloud capture via GitHub Actions.

---

## 🏛️ Directory Hierarchy

```text
India-Stocks-1591-1620-Historical-Data/
├── .github/workflows/daily_ingest.yml
├── fetch_batch.py
├── README.md
├── <SYMBOL>/
│   └── 1m/
│       ├── README.md
│       └── <YYYY>/
│           └── <MM>/
│               ├── <SYMBOL>_1m_<YYYY-MM-DD>.csv
```

---

## ⏰ 4-Tier Automated Schedule (Mon–Fri)

| Trigger | Time (IST) | Cron (UTC) | Role |
|:---|:---:|:---:|:---|
| **Primary Trigger** | **15:45 IST** | `15 10 * * 1-5` | 15 mins post-market close |
| **Backup Trigger 1** | **16:45 IST** | `15 11 * * 1-5` | 1 hour safety net |
| **Backup Trigger 2** | **17:45 IST** | `15 12 * * 1-5` | 2 hours safety net |
| **Backup Trigger 3** | **18:45 IST** | `15 13 * * 1-5` | 3 hours safety net |

---

## 📦 Constituents (1591 to 1620)

| # | Symbol | Company Name | Yahoo Ticker |
|---|---|---|---|
| 1591 | `MAMATA` | Mamata Machinery Limited | `MAMATA.NS` |
| 1592 | `MANAKALUCO` | Manaksia Aluminium Company Limited | `MANAKALUCO.NS` |
| 1593 | `MANAKCOAT` | Manaksia Coated Metals & Industries Limited | `MANAKCOAT.NS` |
| 1594 | `MANAKSIA` | Manaksia Limited | `MANAKSIA.NS` |
| 1595 | `MANAKSTEEL` | Manaksia Steels Limited | `MANAKSTEEL.NS` |
| 1596 | `MANALIPETC` | Manali Petrochemicals Limited | `MANALIPETC.NS` |
| 1597 | `MANBA` | Manba Finance Limited | `MANBA.NS` |
| 1598 | `MANCREDIT` | Mangal Credit and Fincorp Limited | `MANCREDIT.NS` |
| 1599 | `MANGALAM` | Mangalam Drugs And Organics Limited | `MANGALAM.NS` |
| 1600 | `MANGLMCEM` | Mangalam Cement Limited | `MANGLMCEM.NS` |
| 1601 | `MANIKA` | Manika Plastech Limited | `MANIKA.NS` |
| 1602 | `MANINDS` | Man Industries (India) Limited | `MANINDS.NS` |
| 1603 | `MANINFRA` | Man Infraconstruction Limited | `MANINFRA.NS` |
| 1604 | `MANIPALHOS` | Manipal Health Enterprises Limited | `MANIPALHOS.NS` |
| 1605 | `MANOMAY` | Manomay Tex India Limited | `MANOMAY.NS` |
| 1606 | `MANORAMA` | Manorama Industries Limited | `MANORAMA.NS` |
| 1607 | `MANORG` | Mangalam Organics Limited | `MANORG.NS` |
| 1608 | `MANUGRAPH` | Manugraph India Limited | `MANUGRAPH.NS` |
| 1609 | `MANYAVAR` | Vedant Fashions Limited | `MANYAVAR.NS` |
| 1610 | `MAPMYINDIA` | C.E. Info Systems Limited | `MAPMYINDIA.NS` |
| 1611 | `MARALOVER` | Maral Overseas Limited | `MARALOVER.NS` |
| 1612 | `MARATHON` | Marathon Nextgen Realty Limited | `MARATHON.NS` |
| 1613 | `MARINE` | Marine Electricals (India) Limited | `MARINE.NS` |
| 1614 | `MARKOLINES` | Markolines Pavement Technologies Limited | `MARKOLINES.NS` |
| 1615 | `MARKSANS` | Marksans Pharma Limited | `MARKSANS.NS` |
| 1616 | `MARSONS` | Marsons Limited | `MARSONS.NS` |
| 1617 | `MASFIN` | MAS Financial Services Limited | `MASFIN.NS` |
| 1618 | `MASKINVEST` | Mask Investments Limited | `MASKINVEST.NS` |
| 1619 | `MASTEK` | Mastek Limited | `MASTEK.NS` |
| 1620 | `MASTERTR` | Master Trust Limited | `MASTERTR.NS` |


---

## ⚡ 1-Line Pandas Stream Loader

```python
import pandas as pd

# Example: Stream MAMATA 1m data
url = "https://raw.githubusercontent.com/parshant65-lang/India-Stocks-1591-1620-Historical-Data/main/MAMATA/1m/2026/10/MAMATA_1m_2026-10-12.csv"
df = pd.read_csv(url)
print(df.head())
```
