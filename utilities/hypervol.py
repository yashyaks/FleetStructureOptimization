import matplotlib.pyplot as plt
import numpy as np

# --- TOPSIS metrics (previous dictionary) ---
topsis_metrics = {
    2023: {'hypervolume': 84422221073.70848, 'spacing': 20744.218467311388, 'gd': 0.0},
    2024: {'hypervolume': 538091781624.08734, 'spacing': 21572.551606248708, 'gd': 365614.8104568921},
    2025: {'hypervolume': 633013368521.8077, 'spacing': 23150.254730796514, 'gd': 432432.1908512946},
    2026: {'hypervolume': 525198911273.5172, 'spacing': 24240.78593191257, 'gd': 423175.27951196814},
    2027: {'hypervolume': 597208076447.872, 'spacing': 42746.34229869875, 'gd': 547656.8819743503},
    2028: {'hypervolume': 720677709210.6694, 'spacing': 43349.11687791247, 'gd': 503158.3725282012},
    2029: {'hypervolume': 635445850395.7327, 'spacing': 28329.74383994711, 'gd': 393233.4199257556},
    2030: {'hypervolume': -94552056505.99316, 'spacing': 26146.453037094434, 'gd': 403109.35676277074},
    2031: {'hypervolume': 703272196848.4415, 'spacing': 40558.200080084505, 'gd': 610821.1078548252},
    2032: {'hypervolume': 625730399734.4824, 'spacing': 20772.330615942697, 'gd': 452551.3308121842},
    2033: {'hypervolume': 718917644678.733, 'spacing': 25101.59617992754, 'gd': 601696.7530274661},
    2034: {'hypervolume': 720325066784.3917, 'spacing': 26255.644470021536, 'gd': 514129.81384093605},
    2035: {'hypervolume': 618626104097.214, 'spacing': 29042.26276508906, 'gd': 492858.6476262807},
    2036: {'hypervolume': 680349184534.9696, 'spacing': 21991.70104728118, 'gd': 546731.4304016575},
    2037: {'hypervolume': 868277272502.7815, 'spacing': 41164.03582540955, 'gd': 580397.3874122248},
    2038: {'hypervolume': 921717456540.634, 'spacing': 24914.803480370752, 'gd': 705806.0692533556}
}

# --- No-TOPSIS metrics (new dictionary) ---
no_topsis_metrics = {
    2023: {'hypervolume': 102814619551.96013, 'spacing': 17761.88689744538, 'gd': 0.0},
    2024: {'hypervolume': 632352847320.9648, 'spacing': 53918.38483499535, 'gd': 624414.1965303192},
    2025: {'hypervolume': -8820319320.378963, 'spacing': 23840.717563959413, 'gd': 357744.08504775533},
    2026: {'hypervolume': 1059887104222.5344, 'spacing': 34780.51351161589, 'gd': 456032.53449141944},
    2027: {'hypervolume': 572177458111.1371, 'spacing': 45160.70077234126, 'gd': 403497.44692744693},
    2028: {'hypervolume': 1165026638595.5107, 'spacing': 37758.43212634002, 'gd': 581202.8107760254},
    2029: {'hypervolume': 653837647184.1039, 'spacing': 60177.536518453366, 'gd': 560451.4196891214},
    2030: {'hypervolume': 1014810174957.0322, 'spacing': 56861.85700610027, 'gd': 488261.6929080169},
    2031: {'hypervolume': 691420379141.8052, 'spacing': 38260.48324321729, 'gd': 408702.3502096973},
    2032: {'hypervolume': 671349327717.1056, 'spacing': 23541.193516711992, 'gd': 366368.2211827866},
    2033: {'hypervolume': 1238355708460.7122, 'spacing': 33219.916091227424, 'gd': 465851.08120929654},
    2034: {'hypervolume': 1796743618977.5671, 'spacing': 45078.7150345783, 'gd': 650487.2780525668},
    2035: {'hypervolume': 1814037896928.1245, 'spacing': 65495.665401499355, 'gd': 545673.0163451624},
    2036: {'hypervolume': 2157129241939.414, 'spacing': 82332.70913239854, 'gd': 824585.9431428793},
    2037: {'hypervolume': 2160388956013.9924, 'spacing': 61347.99468638356, 'gd': 779141.9392511301},
    2038: {'hypervolume': 1241255055880.9878, 'spacing': 61156.01734122512, 'gd': 808948.5013971799}
}

import matplotlib.pyplot as plt
import numpy as np

# --- Extract years ---
years = sorted(topsis_metrics.keys())

# --- Extract metrics ---
hv_topsis = [topsis_metrics[y]['hypervolume'] for y in years]
sp_topsis = [topsis_metrics[y]['spacing'] for y in years]
gd_topsis = [topsis_metrics[y]['gd'] for y in years]

hv_no = [no_topsis_metrics[y]['hypervolume'] for y in years]
sp_no = [no_topsis_metrics[y]['spacing'] for y in years]
gd_no = [no_topsis_metrics[y]['gd'] for y in years]

# --- Log-scale for hypervolume ---
hv_topsis_log = [np.log10(abs(v)) if v != 0 else 0 for v in hv_topsis]
hv_no_log = [np.log10(abs(v)) if v != 0 else 0 for v in hv_no]

# ---- Plot 1: Hypervolume ----
plt.figure(figsize=(10, 5))
plt.plot(years, hv_topsis_log, marker='o', color='b', label='TOPSIS')
plt.plot(years, hv_no_log, marker='x', color='c', label='No-TOPSIS')
plt.title('Hypervolume (log10) vs Year')
plt.xlabel('Year')
plt.ylabel('log10(Hypervolume)')
plt.grid(True)
plt.legend()
plt.show()

# ---- Plot 2: Spacing ----
plt.figure(figsize=(10, 5))
plt.plot(years, sp_topsis, marker='s', color='g', label='TOPSIS')
plt.plot(years, sp_no, marker='d', color='lime', label='No-TOPSIS')
plt.title('Spacing vs Year')
plt.xlabel('Year')
plt.ylabel('Spacing')
plt.grid(True)
plt.legend()
plt.show()

# ---- Plot 3: Generational Distance ----
plt.figure(figsize=(10, 5))
plt.plot(years, gd_topsis, marker='^', color='r', label='TOPSIS')
plt.plot(years, gd_no, marker='v', color='orange', label='No-TOPSIS')
plt.title('Generational Distance vs Year')
plt.xlabel('Year')
plt.ylabel('GD')
plt.grid(True)
plt.legend()
plt.show()
