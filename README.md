# Multi-Criteria Fleet Optimization

**Minimizing Cost and Carbon Emissions While Meeting Demand**  
A project by Hiya Jain, Yash Thakar, Shruti Jain, Kanchan Dabre
---

## Introduction

Large commercial fleets used for logistics and deliveries contribute significantly to global greenhouse gas (GHG) emissions. This project presents a decision-making framework to support optimal **fleet decarbonization** through **multi-objective optimization**, balancing:

- 📉 Operational cost  
- 🌍 Carbon emissions  
- 📦 Demand satisfaction  

---

## Problem Statement

**Objective:**  
Design a fleet plan that:

- ✅ Minimizes Total Cost of Ownership (TCO)  
- 🌿 Minimizes CO₂ emissions  
- 📈 Satisfies evolving demand year-over-year (2023–2038)  

---

## Methodology

### Multi-Criteria Optimization Framework

1. **Vehicle Data Collection** – Extract key attributes (size, fuel, cost, emissions)  
2. **Vehicle Mapping** – Identify feasible vehicles per demand cluster  
3. **TOPSIS Ranking** – Rank options by acquisition cost, operating cost, and emissions  
4. **NSGA-II Optimization** – Generate Pareto-optimal solutions balancing cost and emissions  
5. **Iterative Planning** – Carry forward fleet to future years, re-evaluating based on need  
6. **Final Output** – Determine optimal fleet combination per year  

### Key Enhancements

- TOPSIS used to **bias population initialization** in NSGA-II  
- Cost and carbon treated as **negative criteria**  
- Existing vehicles reused in future years (zero acquisition cost)  

---

## Architecture

![Architecture Diagram](images/architecture.png)

---

## Parallelization

The algorithm is optimized using **Python's multiprocessing** module:

- Parallelizes size-distance groups across CPU cores  
- Avoids GIL bottlenecks  
- Achieves ~36.2% reduction in runtime  
- No statistically significant difference in results vs sequential  

---

## Hypothesis Testing & Results

### Cost Minimization (50 Runs)
- **p-value = 0.00248**  
- **Null Hypothesis Rejected**  
- TOPSIS-NSGA-II performs significantly better  

### Emissions Minimization (50 Runs)
- **p-value = 0.00303**  
- **Null Hypothesis Rejected**  
- TOPSIS-NSGA-II again outperforms standard NSGA-II  

### Parallel vs Sequential
- **Cost p-value = 0.0969**  
- **Emissions p-value = 0.5106**  
- **Null Hypothesis Accepted**: Parallel execution improves performance without loss in accuracy  

---

## 📊 Performance Comparison

| Metric                          | NSGA-II             | TOPSIS-NSGA-II       | % Improvement |
|-------------------------------|---------------------|----------------------|---------------|
| Total Cost                    | $477,716,970.18     | $342,202,816.90      | 28.37% ↓      |
| Total CO₂ Emissions (kg)     | 188,064,097.70      | 13,444,303.32        | 36.20% ↓      |
| Runtime (Parallel vs Serial) | Longer              | 36.2% Faster         | ✔️            |

---

## 📈 Visual Results

![Results Plot](images/results.png)

---

## 📁 Repository Structure


