import os
import sys
import datetime
import pandas as pd
import yfinance as yf

HEADERS = ["timestamp", "datetime_utc", "open", "high", "low", "close", "volume"]

COMPANIES = {
    "MAMATA": ("Mamata Machinery Limited", "MAMATA.NS"),
    "MANAKALUCO": ("Manaksia Aluminium Company Limited", "MANAKALUCO.NS"),
    "MANAKCOAT": ("Manaksia Coated Metals & Industries Limited", "MANAKCOAT.NS"),
    "MANAKSIA": ("Manaksia Limited", "MANAKSIA.NS"),
    "MANAKSTEEL": ("Manaksia Steels Limited", "MANAKSTEEL.NS"),
    "MANALIPETC": ("Manali Petrochemicals Limited", "MANALIPETC.NS"),
    "MANBA": ("Manba Finance Limited", "MANBA.NS"),
    "MANCREDIT": ("Mangal Credit and Fincorp Limited", "MANCREDIT.NS"),
    "MANGALAM": ("Mangalam Drugs And Organics Limited", "MANGALAM.NS"),
    "MANGLMCEM": ("Mangalam Cement Limited", "MANGLMCEM.NS"),
    "MANIKA": ("Manika Plastech Limited", "MANIKA.NS"),
    "MANINDS": ("Man Industries (India) Limited", "MANINDS.NS"),
    "MANINFRA": ("Man Infraconstruction Limited", "MANINFRA.NS"),
    "MANIPALHOS": ("Manipal Health Enterprises Limited", "MANIPALHOS.NS"),
    "MANOMAY": ("Manomay Tex India Limited", "MANOMAY.NS"),
    "MANORAMA": ("Manorama Industries Limited", "MANORAMA.NS"),
    "MANORG": ("Mangalam Organics Limited", "MANORG.NS"),
    "MANUGRAPH": ("Manugraph India Limited", "MANUGRAPH.NS"),
    "MANYAVAR": ("Vedant Fashions Limited", "MANYAVAR.NS"),
    "MAPMYINDIA": ("C.E. Info Systems Limited", "MAPMYINDIA.NS"),
    "MARALOVER": ("Maral Overseas Limited", "MARALOVER.NS"),
    "MARATHON": ("Marathon Nextgen Realty Limited", "MARATHON.NS"),
    "MARINE": ("Marine Electricals (India) Limited", "MARINE.NS"),
    "MARKOLINES": ("Markolines Pavement Technologies Limited", "MARKOLINES.NS"),
    "MARKSANS": ("Marksans Pharma Limited", "MARKSANS.NS"),
    "MARSONS": ("Marsons Limited", "MARSONS.NS"),
    "MASFIN": ("MAS Financial Services Limited", "MASFIN.NS"),
    "MASKINVEST": ("Mask Investments Limited", "MASKINVEST.NS"),
    "MASTEK": ("Mastek Limited", "MASTEK.NS"),
    "MASTERTR": ("Master Trust Limited", "MASTERTR.NS"),
}


def fetch_and_save_company(symbol, company_name, default_ticker):
    print(f"Fetching 1m data for {symbol} ({company_name})...")
    candidates = [
        default_ticker,
        f"{symbol}.NS",
        f"{symbol.replace('&', '-')}.NS",
        f"{symbol.replace('&', '_')}.NS",
        f"{symbol}.BO"
    ]
    df = None
    for cand in candidates:
        try:
            ticker = yf.Ticker(cand)
            cand_df = ticker.history(period="7d", interval="1m")
            if not cand_df.empty:
                df = cand_df
                break
        except Exception:
            continue

    if df is None or df.empty:
        print(f"No data returned for {symbol} across candidates")
        return False, 0

    rows = []
    for idx, row in df.iterrows():
        ts_utc = idx.to_pydatetime()
        if ts_utc.tzinfo is None:
            ts_utc = ts_utc.replace(tzinfo=datetime.timezone.utc)
        else:
            ts_utc = ts_utc.astimezone(datetime.timezone.utc)

        epoch_ms = int(ts_utc.timestamp() * 1000)
        dt_utc_str = ts_utc.strftime("%Y-%m-%d %H:%M:%S")
        rows.append({
            "timestamp": epoch_ms,
            "datetime_utc": dt_utc_str,
            "open": round(float(row["Open"]), 4),
            "high": round(float(row["High"]), 4),
            "low": round(float(row["Low"]), 4),
            "close": round(float(row["Close"]), 4),
            "volume": int(row["Volume"]),
            "date_utc": ts_utc.strftime("%Y-%m-%d")
        })

    full_df = pd.DataFrame(rows)
    grouped = full_df.groupby("date_utc")
    total_candles = 0

    for date_str, group in grouped:
        year, month, _ = date_str.split("-")
        folder = os.path.join(symbol, "1m", year, month)
        os.makedirs(folder, exist_ok=True)
        csv_path = os.path.join(folder, f"{symbol}_1m_{date_str}.csv")

        to_write = group[HEADERS].copy()
        if os.path.exists(csv_path):
            existing = pd.read_csv(csv_path)
            combined = pd.concat([existing, to_write], ignore_index=True)
            combined = combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
            combined.to_csv(csv_path, index=False)
            total_candles += len(combined)
        else:
            to_write = to_write.sort_values("timestamp")
            to_write.to_csv(csv_path, index=False)
            total_candles += len(to_write)

    # Symbol README
    sym_dir = os.path.join(symbol, "1m")
    os.makedirs(sym_dir, exist_ok=True)
    with open(os.path.join(sym_dir, "README.md"), "w") as f:
        f.write(f"# {symbol} - 1-Minute Historical Kline Data\n\n")
        f.write(f"- **Company Name:** {company_name}\n")
        f.write(f"- **Symbol:** `{symbol}`\n")
        f.write(f"- **Candle Interval:** 1-Minute (`1m`)\n")
        f.write(f"- **Directory Structure:** `<SYMBOL>/1m/<YYYY>/<MM>/<SYMBOL>_1m_<YYYY-MM-DD>.csv`\n")
        f.write(f"- **Schema:** `timestamp,datetime_utc,open,high,low,close,volume`\n")

    return True, total_candles

def main():
    print("Starting automated ingestion for batch...")
    success_count = 0
    total_candles = 0
    for symbol, (cname, ticker) in COMPANIES.items():
        ok, candles = fetch_and_save_company(symbol, cname, ticker)
        if ok:
            success_count += 1
            total_candles += candles
    print(f"Batch completed: {success_count}/{len(COMPANIES)} companies ingested, {total_candles} candles.")

if __name__ == "__main__":
    main()
