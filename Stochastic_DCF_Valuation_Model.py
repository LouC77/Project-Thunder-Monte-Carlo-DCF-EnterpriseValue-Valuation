import numpy as np
import matplotlib.pyplot as plt

# Base assumptions, aligned with the Excel model
current_revenue = 1252.20183    # 2025A revenue = 1364.90 / 1.09
ebit_margin = 0.0476885         # ebit margin 65.09 / 1364.90
tax_rate = 0.15                 # Tax rate = 0.15
wacc = 0.129                    
perpetual_growth = 0.028
projection_years = 5

actual_2025_wc = 409.0          # 2025A working capital
nwc_sales_ratio = 0.286         # WC % of revenue 28.6%

# Mid-year convention
year_fractions = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
discount_factors = 1 / ((1 + wacc) ** year_fractions)

# Simulation parameters
mean_growth = 0.09
std_growth = 0.1677             # sample std of 2023-2025 growth (20.43%, -8.04%, 21.56%)
num_simulations = 10000

simulated_pv_fcf = []
simulated_pv_tv = []
simulated_ev = []

np.random.seed(42)

for _ in range(num_simulations):
    growths = np.random.normal(mean_growth, std_growth, projection_years)

    # Revenue forecast
    revs = []
    temp_rev = current_revenue
    for g in growths:
        temp_rev *= (1 + g)
        revs.append(temp_rev)

    ebit = [r * ebit_margin for r in revs]
    nopat = [e * (1 - tax_rate) for e in ebit]

    # Change in NWC
    nwc_changes = []
    prior_wc = actual_2025_wc
    for r in revs:
        current_wc = r * nwc_sales_ratio
        nwc_changes.append(current_wc - prior_wc)
        prior_wc = current_wc

    fcff = [nopat[i] - nwc_changes[i] for i in range(projection_years)]
    pv_fcff_sum = sum(fcff[i] * discount_factors[i] for i in range(projection_years))

    # Terminal value (Gordon growth)
    terminal_rev = revs[-1] * (1 + perpetual_growth)
    terminal_nopat = terminal_rev * ebit_margin * (1 - tax_rate)
    terminal_nwc_change = (terminal_rev - revs[-1]) * nwc_sales_ratio
    terminal_fcff = terminal_nopat - terminal_nwc_change

    terminal_value = terminal_fcff / (wacc - perpetual_growth)
    pv_terminal_value = terminal_value * discount_factors[-1]

    simulated_pv_fcf.append(pv_fcff_sum)
    simulated_pv_tv.append(pv_terminal_value)
    simulated_ev.append(pv_fcff_sum + pv_terminal_value)

simulated_pv_fcf = np.array(simulated_pv_fcf)
simulated_pv_tv = np.array(simulated_pv_tv)
simulated_ev = np.array(simulated_ev)

# Summary statistics
med_pv_fcf = np.median(simulated_pv_fcf)
med_pv_tv = np.median(simulated_pv_tv)
med_ev = np.median(simulated_ev)
p5_ev = np.percentile(simulated_ev, 5)
p95_ev = np.percentile(simulated_ev, 95)
static_base_ev = 522.17  # Excel base case

print("Stochastic DCF Valuation (USD m)")
print("-" * 50)
print(f"PV of FCF 2026-2030 (median) : {med_pv_fcf:8.2f}")
print(f"PV of terminal value (median): {med_pv_tv:8.2f}")
print(f"Enterprise value (median)    : {med_ev:8.2f}")
print("-" * 50)
print(f"Excel base case EV           : {static_base_ev:8.2f}")
print(f"P5 EV                        : {p5_ev:8.2f}")
print(f"P95 EV                       : {p95_ev:8.2f}")

# Plot EV distribution
plt.figure(figsize=(11, 6), dpi=100)
plt.hist(simulated_ev, bins=80, color='#2b5c8f', alpha=0.75, edgecolor='black', linewidth=0.5)

plt.axvline(med_ev, color='#e74c3c', linestyle='-', linewidth=2.5, label=f'Median EV: ${med_ev:.1f}M')
plt.axvline(static_base_ev, color='#f39c12', linestyle='--', linewidth=2, label=f'Excel Base EV: ${static_base_ev:.1f}M')
plt.axvline(p5_ev, color='#27ae60', linestyle=':', linewidth=2, label=f'P5: ${p5_ev:.1f}M')
plt.axvline(p95_ev, color='#27ae60', linestyle=':', linewidth=2, label=f'P95: ${p95_ev:.1f}M')

plt.suptitle('Stochastic DCF Valuation', fontsize=14, fontweight='bold', y=0.98)
plt.title('EV distribution driven by sales growth uncertainty', fontsize=12, pad=12)
plt.xlabel('Enterprise Value (USD m)', fontsize=11, labelpad=10)
plt.ylabel('Frequency (10,000 simulations)', fontsize=11, labelpad=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')

box_text = (
    f"PV of FCF (2026-2030): ${med_pv_fcf:6.1f}M ({med_pv_fcf / med_ev * 100:.1f}%)\n"
    f"PV of terminal value : ${med_pv_tv:6.1f}M ({med_pv_tv / med_ev * 100:.1f}%)\n"
    f"Enterprise value     : ${med_ev:6.1f}M"
)
plt.gca().text(0.58, 0.65, box_text, transform=plt.gca().transAxes, fontsize=10,
               fontfamily='monospace', verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', edgecolor='#bdc3c7', alpha=0.9))

plt.legend(loc='upper right', fontsize=10, framealpha=0.9)
plt.tight_layout()
plt.show()
