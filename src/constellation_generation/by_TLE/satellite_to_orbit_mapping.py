"""

Author : yunanhou

Date : 2023/12/02

Function : The orbits within a shell are derived based on a clustering algorithm and the satellites are assigned to
           these orbits.

           Specifically, before executing this script, the corresponding relationship between satellites and shells has
           been established, but the relationship between satellites and orbit points has not yet been established. The
           function of this script is to establish the corresponding relationship between satellites and orbit.

           The main function of the script needs to pass in a shell class object, and then cluster the raan of each
           satellite in the shell object to obtain several orbits, and then assign all satellites in the shell to these
           orbits.

"""

import jenkspy
import src.TLE_constellation.constellation_entity.orbit as ORBIT
import matplotlib.pyplot as plt
import numpy as np
import ruptures as rpt
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN


# Automatically detect orbit numbers in RAAN data
def detect_orbit_number(raans: list) -> int:
    """Automatically detect the number of orbits based on RAAN distribution steps

    Inspired by MoE (Mixture of Experts), combining results from various algorithms
    to achieve a robust and reliable estimate of the number of orbits.
    """
    raans = np.array(raans)
    unique_raans = len(np.unique(raans))

    if unique_raans <= 1 or len(raans) < 10:
        return 1

    # Method 1: Enhanced Ruptures with optimal parameters
    def ruptures_detection():
        results = []
        models = ["rbf", "l1", "l2", "normal"]

        for model in models:
            try:
                # PELT with adaptive penalty
                algo = rpt.Pelt(model=model, min_size=max(3, len(raans) // 100))
                algo.fit(raans.reshape(-1, 1))

                # Different penalty strategies
                penalties = [
                    np.log(len(raans)) * 2,  # BIC-like
                    len(raans) ** 0.5,  # Square root penalty
                    len(raans) * 0.01,  # Linear penalty
                ]

                for pen in penalties:
                    try:
                        changepoints = algo.predict(pen=pen)
                        if len(changepoints) > 1:
                            results.append(len(changepoints))
                    except Exception:
                        continue

            except Exception:
                continue

        return results

    # Method 2: Histogram-based plateau detection with smoothing
    def histogram_detection():
        n_bins = max(20, min(len(raans) // 10, 100))
        hist, bin_edges = np.histogram(raans, bins=n_bins)

        # Gaussian smoothing
        smoothed = gaussian_filter1d(hist.astype(float), sigma=1.0)

        # Find peaks
        peaks, _ = find_peaks(
            smoothed,
            height=np.max(smoothed) * 0.05,
            distance=max(1, len(smoothed) // 50),
        )

        return len(peaks) if len(peaks) > 0 else 1

    # Method 3: Gap analysis with statistical significance
    def gap_analysis():
        if len(raans) < 20:
            return 1

        # Calculate gaps
        sorted_raans = np.sort(raans)
        gaps = np.diff(sorted_raans)

        # Find gaps that are outliers using z-score
        if len(gaps) > 0:
            z_scores = np.abs((gaps - np.mean(gaps)) / np.std(gaps))
            significant_gaps = np.sum(z_scores > 2.0)
            return max(1, significant_gaps + 1)

        return 1

    # Method 4: Density-based clustering approach
    def density_clustering():
        try:
            # Reshape for clustering
            raans_reshaped = raans.reshape(-1, 1)

            # Use DBSCAN to find dense regions
            eps = np.std(raans) * 0.1
            db = DBSCAN(eps=eps, min_samples=max(2, len(raans) // 100))
            labels = db.fit_predict(raans_reshaped)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            return max(1, n_clusters)
        except Exception:
            return 1

    # Method 5: Jenks optimization with adaptive classes
    def jenks_optimization():
        best_gvf = 0
        best_k = 1
        max_k = min(len(np.unique(raans)), len(raans) // 5)

        for k in range(1, max_k + 1):
            try:
                breaks = jenkspy.jenks_breaks(raans, n_classes=k)
                gvf = jenkspy.goodness_of_variance_fit(raans, breaks)

                if k == 1:
                    best_gvf = gvf
                    best_k = k
                elif gvf - best_gvf > 0.03:
                    best_gvf = gvf
                    best_k = k
                elif gvf > 0.85 and (gvf - best_gvf) < 0.01:
                    break
            except Exception:
                continue

        return best_k

    # Run all methods
    all_results = []

    try:
        # Ruptures (multiple results)
        ruptures_results = ruptures_detection()
        all_results.extend(ruptures_results)

        # Histogram
        hist_result = histogram_detection()
        all_results.extend([hist_result] * 2)  # More weight

        # Gap analysis
        gap_result = gap_analysis()
        all_results.append(gap_result)

        # Density clustering
        density_result = density_clustering()
        all_results.append(density_result)

        # Jenks optimization
        jenks_result = jenks_optimization()
        all_results.extend([jenks_result] * 2)  # More weight

    except Exception as e:
        print(f"Error in advanced detection: {e}")

    # Robust aggregation
    if all_results:
        # Remove extreme outliers using IQR
        all_results = np.array(all_results)
        q75, q25 = np.percentile(all_results, [75, 25])
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr

        filtered_results = all_results[
            (all_results >= lower_bound) & (all_results <= upper_bound)
        ]

        if len(filtered_results) > 0:
            final_result = int(np.median(filtered_results))
            return max(1, final_result)

    sorted_raans = np.sort(raans)
    gaps = np.diff(sorted_raans)

    if len(gaps) > 0:
        threshold = np.percentile(gaps, 95)
        significant_gaps = np.sum(gaps > threshold)
        return max(1, significant_gaps + 1)

    return 1


# Parameter :
# shells : a collection of shell objects that have established corresponding relationships
# Return Value :
# after the function is executed, the mapping relationship between satellite, orbit, and shell has been established
# without any return value.
def satellite_to_orbit_mapping(shells: list, auto_gen: bool = True) -> None:
    for sh in shells:
        # extract the raan of all satellites in sh
        raans = []
        for sat in sh.satellites:
            raans.append(sat.tle_json["RA_OF_ASC_NODE"])
        raans = sorted(raans)

        orbits_number = 0

        # NOTE: Automatic Mode is recommended for most scenarios especially when dealing with large datasets.
        #       Automatic Mode gains more effectiveness but may sacrifice some accuracy.
        #       Manual Mode offers precision but is more time-consuming.
        if not auto_gen:
            # Manual Mode: visualize RAAN distribution and manually input orbit number
            plt.plot(raans)
            plt.ylabel("RAANS")
            plt.show()
            orbits_number = int(
                input(
                    "\t\t\tPlease enter the number of orbits (integer) based on the raan distribution result of the line chart: "
                )
            )
        else:
            # Automatic Mode: automatically detect orbit number
            orbits_number = detect_orbit_number(raans)
            print(f"\t\t\tAutomatically detected number of orbits: {orbits_number}")

        breaks = jenkspy.jenks_breaks(values=raans, n_classes=orbits_number)
        orbit_raans = [(breaks[i], breaks[i + 1]) for i in range(len(breaks) - 1)]
        for ra_index, ra in enumerate(orbit_raans):
            lower_bound = ra[0]
            upper_bound = ra[1]
            orbit = ORBIT.orbit(
                shell=sh, raan_lower_bound=lower_bound, raan_upper_bound=upper_bound
            )
            for sat in sh.satellites:
                if ra_index > 0:
                    if (
                        sat.tle_json["RA_OF_ASC_NODE"] > lower_bound
                        and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound
                    ):
                        sat.orbit = orbit
                        orbit.satellites.append(sat)
                if ra_index == 0:
                    if (
                        sat.tle_json["RA_OF_ASC_NODE"] >= lower_bound
                        and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound
                    ):
                        sat.orbit = orbit
                        orbit.satellites.append(sat)

            sh.orbits.append(orbit)
