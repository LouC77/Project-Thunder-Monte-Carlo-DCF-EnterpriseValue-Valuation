# Stochastic DCF Valuation Model

> A 10,000-run Monte Carlo DCF framework in Python that quantifies Enterprise Value (EV) probability distributions and downside tail risk under revenue growth uncertainty.

---

## Disclaimer on Data

All financial inputs in this repository (revenue, margins, working capital, growth history, WACC, etc.) are **adjusted and illustrative figures**. They were transformed using formula-based calculations and do **not** represent any actual company, client, or engagement. The project is intended to demonstrate a valuation methodology, not to value a real entity. Results should not be interpreted as an investment or valuation opinion.

---

## Motivation & Background

In practice, DCF forecasts often rely on a **single, deterministic annual sales growth rate**, frequently a static industry CAGR taken from equity research reports, applied across the entire projection period.

A static CAGR simplifies baseline modeling, but it assumes zero operational volatility. In cyclical sectors such as semiconductors, a deterministic growth assumption does not capture market fluctuations, macroeconomic shocks, or downside tail risk. The result is a single Enterprise Value that can convey more precision than the underlying assumptions justify.

To bridge traditional corporate valuation with quantitative risk modeling, I built this **Stochastic DCF framework** in Python:

* **Expected growth ($\mu = 9.0\%$)**: Keeps the research-consensus CAGR as the mean of annual sales growth.
* **Growth volatility ($\sigma = 16.77\%$)**: Estimated as the sample standard deviation of three years of historical annual revenue growth (+20.43%, -8.04%, +21.56%).
* **Stochastic simulation**: Draws 10,000 random five-year growth paths (negative-growth scenarios included) and recomputes revenue, NOPAT, change in net working capital, free cash flow, and EV on each path.

By moving from a single-point estimate to a full **EV probability distribution**, the model gives decision-makers quantified risk boundaries ($P_5$ downside vs. $P_{95}$ upside) to support deal pricing and strategic evaluation.

---

## Key Features & Methodology

* **Mid-year discounting convention**: Cash flows discounted at $t = 0.5, 1.5, 2.5, 3.5, 4.5$ with $WACC = 12.9\%$.
* **Working capital dynamics**: Net working capital is set at 28.6% of revenue, so revenue contractions ($g < 0$) automatically release working capital as a cash inflow.
* **Terminal value**: Gordon Growth at a 2.8% perpetual growth rate. Terminal-year NWC investment is recalculated from the normalized growth rate instead of scaling Year 5 FCF, which avoids carrying high projection-period growth into perpetuity.
* **Reproducibility**: Random seed fixed at 42.

### Model Inputs

| Parameter | Value |
| :--- | :--- |
| Base-year revenue (2025A) | $1,252.2M |
| EBIT margin | 4.77% |
| Tax rate | 15% |
| WACC | 12.9% |
| Perpetual growth rate | 2.8% |
| NWC as % of revenue | 28.6% |
| Projection period | 5 years (2026–2030) |
| Simulations | 10,000 |

---

## Valuation Results & Simulation Output


### Key Metrics Summary (USD in Millions)

| Metric | Enterprise Value | Description |
| :--- | :--- | :--- |
| **Excel Base EV** | **$522.2M** | Static DCF with a fixed 9.0% growth rate |
| **Simulated Median EV** | **$516.0M** | 50th percentile of 10,000 simulation runs |
| **P5 Downside** | **$462.9M** | 5th percentile of simulated EV |
| **P95 Upside** | **$596.7M** | 95th percentile of simulated EV |

$P_5$ to $P_{95}$ covers the central 90% of simulated outcomes.

**Valuation component breakdown (median):**
* PV of explicit forecast (2026–2030): $161.7M (~31.3%)
* PV of terminal value: $354.4M (~68.7%)

---

## Limitations & Possible Extensions

This is a proof-of-concept and has several simplifications:

* **Only revenue growth is stochastic.** WACC, EBIT margin, tax rate, and terminal growth are held constant, so the distribution likely understates total valuation uncertainty.
*
