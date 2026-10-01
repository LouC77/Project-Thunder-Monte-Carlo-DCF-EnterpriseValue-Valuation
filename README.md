# Project Thunder: Stochastic DCF Valuation Model

> A 10,000-run Monte Carlo DCF valuation framework in Python designed to quantify Enterprise Value (EV) probability distributions and downside tail risks under revenue growth uncertainty.

---

## Motivation & Background

While conducting a valuation engagement for a semiconductor transaction, I identified a critical structural limitation in traditional Discounted Cash Flow (DCF) models: practitioners and clients frequently rely on a **single, deterministic annual sales growth rate**—often a static industry CAGR derived from equity research reports—across the entire projection period.

While a static CAGR simplifies baseline modeling, it operates on the unrealistically rigid assumption of zero operational volatility. In cyclical sectors like semiconductors, a deterministic growth assumption fails to account for market fluctuations, macroeconomic shocks, and downside tail risks.

To bridge traditional corporate valuation with quantitative risk management, I developed this **Stochastic Monte Carlo DCF Framework** in Python:

* **Baseline Target ($\mu = 9.0\%$)**: Retains the management-guided / research consensus CAGR as the expected mean for annual sales growth.
* **Empirical Volatility Calibration ($\sigma = 16.77\%$)**: Calibrates parameter variance using the sample standard deviation of historical annual revenue growth (+20.43%, -8.04%, +21.56%) sourced from financial statements.
* **Stochastic Simulation**: Executes 10,000 randomized growth trajectories, capturing non-linear Working Capital ($\Delta\text{NWC}$) dynamics during both expansionary and contractionary cycles.

By transitioning from a single-point estimate to a full **Enterprise Value (EV) probability distribution**, this model provides decision-makers with quantified risk boundaries ($P_5$ downside risk vs. $P_{95}$ upside potential), offering a significantly more robust foundation for deal pricing and strategic evaluation.

---

## Key Features & Financial Methodology

* **Mid-Year Discounting Convention**: Applied exact mid-year discount factors ($t = 0.5, 1.5, 2.5, 3.5, 4.5$) with $WACC = 12.9\%$ to align with institutional investment banking standards.
* **Dynamic Working Capital Buffer**: Implemented adaptive $\Delta\text{NWC}$ calculations where revenue contractions ($g < 0$) automatically release working capital into cash inflows, mimicking real-world liquidity dynamics.
* **Terminal Value Calibration**: Re-calculated Terminal NWC requirements based on a normalized 2.8% perpetual growth rate rather than directly multiplying Year 5 FCF, eliminating distortions from high projection-period growth assumptions.

---

## Valuation Results & Simulation Output

<img width="1100" height="589" alt="image" src="https://github.com/user-attachments/assets/73913529-aaa0-49ff-91c4-882bb07e0428" />



### Key Metrics Summary (USD in Millions)

| Metric | Enterprise Value | Methodology / Description |
| :--- | :--- | :--- |
| **Excel Base EV** | **$522.2M** | Static DCF with fixed 9.0% growth rate |
| **Simulated Median EV** | **$516.0M** | 50th percentile of 10,000 Monte Carlo runs |
| **P5 Downside Risk** | **$462.9M** | 5th percentile (95% confidence lower bound) |
| **P95 Upside Potential** | **$596.7M** | 95th percentile (95% confidence upper bound) |

* **Valuation Component Breakdown**:
  * **PV of Explicit Forecast (2026–2030)**: $161.7M (~31.3%)
  * **PV of Terminal Value**: $354.4M (~68.7%)

---
