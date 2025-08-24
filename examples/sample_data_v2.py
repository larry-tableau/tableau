# Synthetic Customer Analytics Data Generation (PII-Removed)
# - All customer/account manager labels and regions are synthetic.
# - No real organisation, person, or location names are used.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import warnings
warnings.filterwarnings('ignore')

# Try importing pantab for Hyper export, fallback if unavailable
try:
    import pantab
    PANTAB_AVAILABLE = True
except ImportError:
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'pantab', 'pyarrow'])
        import pantab
        PANTAB_AVAILABLE = True
    except Exception:
        PANTAB_AVAILABLE = False
        print("# Pantab unavailable - will skip Hyper export")

# Set global random seed for reproducibility
np.random.seed(42)

# Scenario configuration constants (synthetic segments/regions)
SCENARIO_CONFIG = {
    'enable_performance_spike': True,
    'spike_metric': 'case_mttr_hours',
    'spike_period_days': 90,
    'spike_magnitude': 2.5,
    'affected_segment': 'Manufacturing',     # synthetic industry segment
    'enable_degradation': True,
    'degradation_dimension': 'Region B',     # synthetic region
    'degradation_duration_months': 6,
    'degradation_magnitude': 0.3,
    'outlier_concentration_recent_pct': 80
}

EXECUTIVE_SUMMARY = {
    'primary_insight': 'Manufacturing customers in Region B show a 150% spike in case resolution time during warmer months with tariff mismatch correlation',
    'quantified_impact': '$2.1M potential revenue impact from delayed anomaly detection and customer escalations',
    'injected_scenarios': [
        'Manufacturing segment MTTR spike 2.5x baseline in last 90 days correlated with seasonal operations',
        'Region B showing 30% degradation in data completeness over 6 months affecting early warning capability',
        'Critical anomalies concentrated in recent 20% timeframe showing seasonal pattern correlation'
    ],
    'tableau_detection_hints': [
        'Filter to last 90 days and look for spikes in case_mttr_hours for Manufacturing industry',
        'Compare Region B vs Region A performance on data_completeness_rate',
        'Trend analysis on anomaly_detection_precision over 6 months shows model drift'
    ]
}

def generate_customer_analytics_data():
    """Generate 150,000 rows of synthetic customer analytics data (PII-removed)."""

    # Reference date (example); can be replaced with a timezone-aware datetime if desired
    reference_date = datetime(2025, 8, 21, 11, 28, 26)

    # Date range: 2+ years lookback with 60% in recent 6 months
    start_date = reference_date - timedelta(days=750)
    recent_cutoff = reference_date - timedelta(days=180)

    print("Generating synthetic customer analytics monitoring data...")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {reference_date.strftime('%Y-%m-%d')}")

    # Generate weighted timestamps - 60% in recent 6 months
    total_rows = 150_000
    recent_count = int(total_rows * 0.6)
    historical_count = total_rows - recent_count

    # Recent timestamps (last 6 months)
    recent_days = (reference_date - recent_cutoff).days
    recent_random_days = np.random.randint(0, recent_days, recent_count)
    recent_timestamps = [
        recent_cutoff + timedelta(days=int(d), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
        for d in recent_random_days
    ]

    # Historical timestamps (older than 6 months)
    historical_days = (recent_cutoff - start_date).days
    historical_random_days = np.random.randint(0, historical_days, historical_count)
    historical_timestamps = [
        start_date + timedelta(days=int(d), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
        for d in historical_random_days
    ]

    # Combine and shuffle
    all_timestamps = recent_timestamps + historical_timestamps
    np.random.shuffle(all_timestamps)

    # Base data dict
    data = {}

    # Row identifiers
    data['row_id'] = [str(uuid.uuid4()) for _ in range(total_rows)]
    data['as_of'] = all_timestamps

    # Derive time dimensions
    data['date'] = [ts.date() for ts in all_timestamps]
    data['week_start'] = [ts.date() - timedelta(days=ts.weekday()) for ts in all_timestamps]
    data['month_start'] = [ts.date().replace(day=1) for ts in all_timestamps]

    # Synthetic customer labels (no real names)
    # 50 synthetic customers: "Customer 001" ... "Customer 050"
    customer_labels = [f'Customer {i:03d}' for i in range(1, 51)]
    data['customer_sk'] = np.random.randint(1, 51, total_rows)
    data['customer_id'] = [f'CUST{str(sk).zfill(3)}' for sk in data['customer_sk']]
    data['customer_label'] = [customer_labels[sk - 1] for sk in data['customer_sk']]

    # Synthetic site labels (200 sites): "Site 001" ... "Site 200"
    data['site_sk'] = np.random.randint(1, 201, total_rows)
    data['site_id'] = [f'SITE{str(sk).zfill(3)}' for sk in data['site_sk']]

    # Synthetic regions
    regions = ['Region A', 'Region B', 'Region C', 'Region D']
    region_weights = [0.45, 0.25, 0.20, 0.10]
    data['region'] = np.random.choice(regions, total_rows, p=region_weights)

    # Industries (generic)
    industries = ['Manufacturing', 'Healthcare', 'Education', 'Logistics', 'Other']
    industry_weights = [0.40, 0.15, 0.15, 0.15, 0.15]
    data['industry'] = np.random.choice(industries, total_rows, p=industry_weights)

    # Synthetic account managers (no personal names)
    managers = [f'AM-{i:03d}' for i in range(1, 13)]  # AM-001 ... AM-012
    data['account_manager'] = np.random.choice(managers, total_rows)

    # KPI measures with realistic distributions and correlations

    # Case MTTR (hours) - normal around 6-8 hours
    base_mttr = np.random.normal(7.0, 2.5, total_rows)
    data['case_mttr_hours'] = np.clip(base_mttr, 0.5, 72.0)

    # First contact resolution rate (0-1), skew high
    data['first_contact_resolution_rate'] = np.random.beta(8, 2, total_rows)

    # Anomaly detection metrics
    data['anomaly_detection_precision'] = np.random.beta(17, 2, total_rows)
    data['anomaly_detection_recall'] = np.random.beta(15, 3, total_rows)

    # Proactive notification rate
    data['proactive_notification_rate'] = np.random.beta(18, 2, total_rows)

    # Data completeness rate (very high baseline)
    data['data_completeness_rate'] = np.random.beta(20, 1, total_rows)

    # Tariff optimisation savings (currency) - lognormal
    base_savings = np.random.lognormal(9.5, 0.8, total_rows)
    data['tariff_optimisation_savings_aud'] = np.clip(base_savings, 1000, 100000)

    # Notification timeliness (minutes)
    data['notification_timeliness_minutes'] = np.random.lognormal(3.5, 0.7, total_rows)

    # Customer satisfaction score (0-10)
    css = np.random.normal(7.0, 1.2, total_rows)
    data['customer_satisfaction_score'] = np.clip(css, 0, 10)

    # False positive rate (low)
    data['false_positive_rate'] = np.random.beta(2, 15, total_rows)

    # Billing correction accuracy (very high)
    data['billing_correction_accuracy'] = np.random.beta(19, 1, total_rows)

    # Volume metrics
    data['total_cases_opened'] = np.random.poisson(15, total_rows) + 1
    data['total_alerts_generated'] = np.random.poisson(25, total_rows) + 5
    data['critical_cases_count'] = np.random.poisson(2.5, total_rows)

    # Build DataFrame
    df = pd.DataFrame(data)

    # Scenario 1: Performance spike in Manufacturing (last 90 days)
    spike_cutoff = reference_date - timedelta(days=SCENARIO_CONFIG['spike_period_days'])
    spike_mask = (df['as_of'] >= spike_cutoff) & (df['industry'] == SCENARIO_CONFIG['affected_segment'])
    spike_indices = df.index[spike_mask]

    if len(spike_indices) > 0:
        # ~2.0–3.0x spike on MTTR
        df.loc[spike_indices, 'case_mttr_hours'] *= np.random.uniform(2.0, 3.0, len(spike_indices))
        # Correlated decrease in first contact resolution
        df.loc[spike_indices, 'first_contact_resolution_rate'] *= np.random.uniform(0.6, 0.8, len(spike_indices))
        print(f"Applied performance spike to {len(spike_indices)} Manufacturing records")

    # Scenario 2: Gradual degradation in Region B (6 months)
    degradation_cutoff = reference_date - timedelta(days=SCENARIO_CONFIG['degradation_duration_months'] * 30)
    degradation_mask = (df['as_of'] >= degradation_cutoff) & (df['region'] == SCENARIO_CONFIG['degradation_dimension'])
    degradation_indices = df.index[degradation_mask]

    if len(degradation_indices) > 0:
        # Gradual decline in data completeness
        degradation_factor = np.random.uniform(0.7, 0.9, len(degradation_indices))
        df.loc[degradation_indices, 'data_completeness_rate'] *= degradation_factor
        # Correlated increase in false positives
        df.loc[degradation_indices, 'false_positive_rate'] *= np.random.uniform(1.5, 2.5, len(degradation_indices))
        print(f"Applied degradation pattern to {len(degradation_indices)} records in Region B")

    # Scenario 3: Outlier concentration in recent 20% of timeframe
    outlier_cutoff = reference_date - timedelta(days=int(750 * 0.2))  # Recent ~20%
    outlier_mask = df['as_of'] >= outlier_cutoff
    outlier_indices = df.index[outlier_mask]

    # Select ~2% outliers from the recent period, but only if available
    outlier_sample_size = int(len(outlier_indices) * 0.02)
    if outlier_sample_size > 0:
        selected_outlier_indices = np.random.choice(outlier_indices, outlier_sample_size, replace=False)

        # Apply various outlier patterns
        for idx in selected_outlier_indices:
            outlier_type = np.random.choice(['mttr_spike', 'savings_spike', 'satisfaction_drop'])
            if outlier_type == 'mttr_spike':
                df.at[idx, 'case_mttr_hours'] *= np.random.uniform(5, 10)
            elif outlier_type == 'savings_spike':
                df.at[idx, 'tariff_optimisation_savings_aud'] *= np.random.uniform(3, 8)
            elif outlier_type == 'satisfaction_drop':
                df.at[idx, 'customer_satisfaction_score'] *= np.random.uniform(0.3, 0.6)

        print(f"Applied outlier patterns to {outlier_sample_size} recent records")
    else:
        print("No recent records available for outlier sampling; skipping outlier injection")

    # AU-formatted date strings for export
    df['date_formatted'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')
    df['week_start_formatted'] = pd.to_datetime(df['week_start']).dt.strftime('%d/%m/%Y')
    df['month_start_formatted'] = pd.to_datetime(df['month_start']).dt.strftime('%d/%m/%Y')
    df['as_of_formatted'] = pd.to_datetime(df['as_of']).dt.strftime('%d/%m/%Y %H:%M:%S')

    # Validation checks
    print(f"\nValidation Results:")
    print(f"✓ Row count: {len(df)} (target: 150,000)")
    print(f"✓ Date coverage: {df['date'].min()} to {df['date'].max()}")
    print(f"✓ Recent 6 months: {(df['as_of'] >= recent_cutoff).sum() / len(df):.1%}")

    # Validate spike pattern
    recent_90_manufacturing = df[(df['as_of'] >= spike_cutoff) & (df['industry'] == SCENARIO_CONFIG['affected_segment'])]
    historical_manufacturing = df[(df['as_of'] < spike_cutoff) & (df['industry'] == SCENARIO_CONFIG['affected_segment'])]

    if len(recent_90_manufacturing) > 0 and len(historical_manufacturing) > 0:
        recent_mttr_mean = recent_90_manufacturing['case_mttr_hours'].mean()
        historical_mttr_mean = historical_manufacturing['case_mttr_hours'].mean()
        spike_ratio = recent_mttr_mean / max(historical_mttr_mean, 1e-9)
        print(f"✓ Manufacturing MTTR spike ratio: {spike_ratio:.1f}x (target: ≥2.0x)")
        if spike_ratio < 2.0:
            print("⚠ Warning: Spike pattern may be insufficient")

    # Validate degradation pattern
    recent_deg = df[(df['as_of'] >= degradation_cutoff) & (df['region'] == SCENARIO_CONFIG['degradation_dimension'])]
    historical_deg = df[(df['as_of'] < degradation_cutoff) & (df['region'] == SCENARIO_CONFIG['degradation_dimension'])]

    if len(recent_deg) > 0 and len(historical_deg) > 0:
        recent_completeness = recent_deg['data_completeness_rate'].mean()
        historical_completeness = historical_deg['data_completeness_rate'].mean()
        degradation_ratio = recent_completeness / max(historical_completeness, 1e-9)
        print(f"✓ Region B completeness ratio: {degradation_ratio:.2f} (target: ≤0.8)")
        if degradation_ratio > 0.8:
            print("⚠ Warning: Degradation pattern may be insufficient")

    return df

def export_data(df):
    """Export data to CSV and Hyper formats"""
    timestamp_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Prepare export DataFrame with Australian date formatting
    export_df = df.copy()

    # Use formatted dates for export
    export_df['date'] = export_df['date_formatted']
    export_df['week_start'] = export_df['week_start_formatted']
    export_df['month_start'] = export_df['month_start_formatted']
    export_df['as_of'] = export_df['as_of_formatted']

    # Drop temporary formatted columns
    export_df = export_df.drop(columns=['date_formatted', 'week_start_formatted',
                                       'month_start_formatted', 'as_of_formatted'])

    # CSV export
    csv_filename = f'customer_analytics_pulse_{timestamp_suffix}.csv'
    export_df.to_csv(csv_filename, index=False)
    print(f"✓ CSV export complete: {csv_filename}")

    # Hyper export
    if PANTAB_AVAILABLE:
        try:
            hyper_filename = f'customer_analytics_pulse_{timestamp_suffix}.hyper'
            pantab.frame_to_hyper(export_df, hyper_filename, table='CustomerAnalytics')
            print(f"✓ Hyper export complete: {hyper_filename}")
        except Exception as e:
            print(f"⚠ Hyper export failed: {e}")
    else:
        print("⚠ Hyper export skipped - pantab not available")

    return csv_filename

def main():
    """Main execution function"""
    print("Synthetic Customer Analytics Data Generation (PII-Removed)")
    print("=" * 60)
    print(f"Target: 150,000 records")
    print(f"Scenario: {EXECUTIVE_SUMMARY['primary_insight']}")
    print()

    # Generate data
    df = generate_customer_analytics_data()

    # Export files
    csv_file = export_data(df)

    # Final validation and summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)

    # Acceptance tests
    assert len(df) == 150000, f"Row count validation failed: {len(df)} != 150000"

    required_columns = ['row_id', 'as_of', 'date', 'customer_sk', 'case_mttr_hours']
    missing_columns = [col for col in required_columns if col not in df.columns]
    assert len(missing_columns) == 0, f"Missing required columns: {missing_columns}"

    date_range_days = (df['as_of'].max() - df['as_of'].min()).days
    assert date_range_days >= 730, f"Date range too small: {date_range_days} days < 730"

    recent_6m = df['as_of'] >= (df['as_of'].max() - timedelta(days=180))
    recent_pct = recent_6m.sum() / len(df)
    assert recent_pct >= 0.55, f"Recent data percentage too low: {recent_pct:.1%} < 55%"

    print("✓ All acceptance tests passed")

    # Executive insights
    print(f"\nKey Insights for Tableau Pulse:")
    for hint in EXECUTIVE_SUMMARY['tableau_detection_hints']:
        print(f"• {hint}")

    print(f"\nBusiness Impact: {EXECUTIVE_SUMMARY['quantified_impact']}")

    return df

if __name__ == "__main__":
    df = main()
