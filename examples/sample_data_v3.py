import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytz
import uuid
import subprocess
import sys

np.random.seed(42)

SCENARIO_CONFIG = {
    'enable_performance_spike': True,
    'spike_metric': 'demand_index',
    'spike_period_days': 90,
    'spike_magnitude': 2.5,
    'affected_segment': 'Hunter Valley',
    'affected_segment_type': 'sa3_name',
    'enable_degradation': True,
    'degradation_metric': 'coverage_ratio',
    'degradation_dimension': 'state',
    'degradation_segment': 'QLD',
    'degradation_duration_months': 6,
    'degradation_magnitude': 0.25,
    'enable_anomaly': True,
    'anomaly_metric': 'travel_minutes_per_visit',
    'anomaly_dimension': 'state',
    'anomaly_segment': 'NT',
    'anomaly_variance': 0.45,
    'outlier_concentration_recent_pct': 80
}

EXECUTIVE_SUMMARY = {
    'primary_insight': 'Hunter Valley demand has surged, exposing Queensland coverage erosion and NT travel drag.',
    'quantified_impact': 'Rebalancing Connected Care deployment across Hunter Valley and Queensland corridors protects ~$42M in potential revenue uplift while trimming 4.5K annual travel hours.',
    'injected_scenarios': [
        'Spike: demand_index increased 2.5× in Hunter Valley over the last 90 days',
        'Degradation: coverage_ratio declined 25% in QLD over 6 months',
        'Anomaly: NT travel_minutes_per_visit shows ~45% variance vs national baseline'
    ],
    'tableau_detection_hints': [
        'Filter to last 90 days and SA3 = Hunter Valley to see the demand_index spike',
        'Trend coverage_ratio by state; Queensland shows the sharpest drop post-May 2025',
        'Compare travel_minutes_per_visit for NT vs national average across the last quarter'
    ]
}

def ensure_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package_name])
        __import__(package_name)

ref_date = pd.to_datetime('16/11/2025', format='%d/%m/%Y')
start_date = (ref_date - timedelta(days=730)).replace(day=1)
recent_6mo_date = ref_date - timedelta(days=180)
spike_start_date = ref_date - timedelta(days=SCENARIO_CONFIG['spike_period_days'])
degradation_start_date = ref_date - timedelta(days=SCENARIO_CONFIG['degradation_duration_months'] * 30)

STATE_TARGETS = {
    'NSW': 320,
    'VIC': 280,
    'QLD': 260,
    'SA': 140,
    'WA': 200,
    'TAS': 80,
    'NT': 60,
    'ACT': 160
}

STATE_CONFIG = {
    'NSW': [
        {'sa3_name': 'Hunter Valley', 'region_type': 'regional'},
        {'sa3_name': 'Newcastle', 'region_type': 'metro'},
        {'sa3_name': 'Central Coast', 'region_type': 'metro'},
        {'sa3_name': 'Riverina', 'region_type': 'rural'},
        {'sa3_name': 'Illawarra', 'region_type': 'metro'}
    ],
    'VIC': [
        {'sa3_name': 'Melbourne Inner', 'region_type': 'metro'},
        {'sa3_name': 'Geelong', 'region_type': 'regional'},
        {'sa3_name': 'Gippsland', 'region_type': 'rural'},
        {'sa3_name': 'Ballarat', 'region_type': 'regional'},
        {'sa3_name': 'Mornington Peninsula', 'region_type': 'metro'}
    ],
    'QLD': [
        {'sa3_name': 'Brisbane South', 'region_type': 'metro'},
        {'sa3_name': 'Gold Coast', 'region_type': 'metro'},
        {'sa3_name': 'Sunshine Coast', 'region_type': 'regional'},
        {'sa3_name': 'Wide Bay', 'region_type': 'rural'},
        {'sa3_name': 'Townsville', 'region_type': 'regional'}
    ],
    'SA': [
        {'sa3_name': 'Adelaide Central', 'region_type': 'metro'},
        {'sa3_name': 'Barossa', 'region_type': 'regional'},
        {'sa3_name': 'Fleurieu - Kangaroo Island', 'region_type': 'regional'},
        {'sa3_name': 'Limestone Coast', 'region_type': 'rural'}
    ],
    'WA': [
        {'sa3_name': 'Perth South', 'region_type': 'metro'},
        {'sa3_name': 'Perth North', 'region_type': 'metro'},
        {'sa3_name': 'South West WA', 'region_type': 'regional'},
        {'sa3_name': 'Pilbara', 'region_type': 'remote'},
        {'sa3_name': 'Kimberley', 'region_type': 'remote'}
    ],
    'TAS': [
        {'sa3_name': 'Hobart', 'region_type': 'metro'},
        {'sa3_name': 'Launceston and North East', 'region_type': 'regional'},
        {'sa3_name': 'North West', 'region_type': 'regional'},
        {'sa3_name': 'West Coast', 'region_type': 'remote'}
    ],
    'NT': [
        {'sa3_name': 'Darwin', 'region_type': 'metro'},
        {'sa3_name': 'Alice Springs', 'region_type': 'remote'},
        {'sa3_name': 'Katherine', 'region_type': 'remote'}
    ],
    'ACT': [
        {'sa3_name': 'Canberra North', 'region_type': 'metro'},
        {'sa3_name': 'Canberra South', 'region_type': 'metro'},
        {'sa3_name': 'Belconnen', 'region_type': 'metro'},
        {'sa3_name': 'Tuggeranong', 'region_type': 'metro'}
    ]
}

descriptor_words = [
    'Heights', 'Central', 'Gardens', 'Foothills', 'Plains',
    'Harbour', 'North', 'South', 'Ridge', 'Waters',
    'Vista', 'Meadows', 'Outlook', 'Grove', 'Lakes'
]

def generate_profile(region_type):
    if region_type == 'metro':
        base_erp = np.random.randint(3500, 6200)
        base_need_rate = np.random.uniform(0.09, 0.14)
        base_diabetes = np.random.uniform(0.055, 0.09)
        base_ckd = np.random.uniform(0.035, 0.055)
        seifa = np.random.uniform(0.5, 0.85)
        income_base = np.random.randint(75000, 105000)
        calvary_sites_base = np.random.uniform(1.2, 3.8)
        competitor_sites_base = np.random.uniform(2.5, 6.5)
        rac_beds_base = np.random.uniform(260, 620)
        travel_base = np.random.uniform(18, 26)
        risk_base = np.random.uniform(40, 65)
    elif region_type == 'regional':
        base_erp = np.random.randint(2200, 4200)
        base_need_rate = np.random.uniform(0.11, 0.16)
        base_diabetes = np.random.uniform(0.065, 0.105)
        base_ckd = np.random.uniform(0.04, 0.06)
        seifa = np.random.uniform(0.35, 0.7)
        income_base = np.random.randint(65000, 90000)
        calvary_sites_base = np.random.uniform(1, 3)
        competitor_sites_base = np.random.uniform(2, 5.5)
        rac_beds_base = np.random.uniform(220, 680)
        travel_base = np.random.uniform(24, 36)
        risk_base = np.random.uniform(45, 70)
    elif region_type == 'rural':
        base_erp = np.random.randint(1400, 2800)
        base_need_rate = np.random.uniform(0.12, 0.17)
        base_diabetes = np.random.uniform(0.07, 0.11)
        base_ckd = np.random.uniform(0.045, 0.065)
        seifa = np.random.uniform(0.25, 0.55)
        income_base = np.random.randint(55000, 75000)
        calvary_sites_base = np.random.uniform(0.5, 2.2)
        competitor_sites_base = np.random.uniform(1, 4.2)
        rac_beds_base = np.random.uniform(150, 520)
        travel_base = np.random.uniform(30, 45)
        risk_base = np.random.uniform(50, 78)
    else:
        base_erp = np.random.randint(900, 2000)
        base_need_rate = np.random.uniform(0.13, 0.18)
        base_diabetes = np.random.uniform(0.08, 0.12)
        base_ckd = np.random.uniform(0.05, 0.07)
        seifa = np.random.uniform(0.12, 0.4)
        income_base = np.random.randint(50000, 70000)
        calvary_sites_base = np.random.uniform(0.3, 1.5)
        competitor_sites_base = np.random.uniform(1, 3.5)
        rac_beds_base = np.random.uniform(120, 360)
        travel_base = np.random.uniform(40, 60)
        risk_base = np.random.uniform(55, 80)
    growth_rate = np.random.uniform(0.008, 0.015)
    income_growth = np.random.uniform(0.02, 0.035)
    return {
        'base_erp': base_erp,
        'base_need_rate': base_need_rate,
        'base_diabetes': base_diabetes,
        'base_ckd': base_ckd,
        'seifa': seifa,
        'income_base': income_base,
        'income_growth': income_growth,
        'calvary_sites_base': calvary_sites_base,
        'competitor_sites_base': competitor_sites_base,
        'rac_beds_base': rac_beds_base,
        'travel_base': travel_base,
        'risk_base': risk_base,
        'growth_rate': growth_rate
    }

sa2_profiles = []
code_counter = 200000000
descriptor_index = 0

for state, target in STATE_TARGETS.items():
    sa3_entries = STATE_CONFIG[state]
    base_count = target // len(sa3_entries)
    remainder = target % len(sa3_entries)
    for idx, sa3 in enumerate(sa3_entries):
        allocation = base_count + (1 if idx < remainder else 0)
        for i in range(allocation):
            descriptor = descriptor_words[descriptor_index % len(descriptor_words)]
            descriptor_index += 1
            sa2_name = f"{sa3['sa3_name']} {descriptor} {((i % 4) + 1)}"
            base_metrics = generate_profile(sa3['region_type'])
            sa2_profiles.append({
                'sa2_code': f"{code_counter:09d}",
                'sa2_name': sa2_name,
                'sa3_name': sa3['sa3_name'],
                'state': state,
                'region_type': sa3['region_type'],
                **base_metrics
            })
            code_counter += 1

assert len(sa2_profiles) == 1500, "SA2 profile count mismatch"

SA2_TOTAL = len(sa2_profiles)
DAILY_SA2_COUNT = 786
MIDWEEK_SA2_COUNT = 1170
BASE_ROWS = SA2_TOTAL * 64
TOTAL_ROWS_EXPECTED = BASE_ROWS + DAILY_SA2_COUNT * 30 + MIDWEEK_SA2_COUNT * 26
assert TOTAL_ROWS_EXPECTED == 150000, "Planned row count mismatch"

weekly_dates = pd.date_range(end=ref_date, periods=52, freq='W-SUN')
midweek_dates = pd.date_range(end=ref_date, periods=26, freq='W-WED')
monthly_dates = pd.date_range(start=start_date, periods=12, freq='MS')

daily_selection = np.random.permutation(SA2_TOTAL)
daily_set = set(daily_selection[:DAILY_SA2_COUNT])

midweek_selection = np.random.permutation(SA2_TOTAL)
midweek_set = set(midweek_selection[:MIDWEEK_SA2_COUNT])

def build_daily_dates(exclude_days):
    collected = []
    day_offset = 0
    while len(collected) < 30:
        candidate = ref_date - timedelta(days=int(day_offset))
        if candidate.weekday() not in exclude_days:
            collected.append(candidate)
        day_offset += 1
        if day_offset > 120 and len(collected) < 30:
            raise ValueError("Unable to generate required daily dates without overlap")
    collected.sort()
    return collected

rows = []
for idx, profile in enumerate(sa2_profiles):
    date_set = set(monthly_dates)
    date_set.update(weekly_dates)
    if idx in midweek_set:
        date_set.update(midweek_dates)
    if idx in daily_set:
        exclude_days = {6}
        if idx in midweek_set:
            exclude_days.add(2)
        daily_dates = build_daily_dates(exclude_days)
        for dt in daily_dates:
            date_set.add(pd.Timestamp(dt))
    expected_dates = 64 + (26 if idx in midweek_set else 0) + (30 if idx in daily_set else 0)
    if len(date_set) != expected_dates:
        raise ValueError(f"Date collision detected for SA2 index {idx}")
    for date_ts in sorted(date_set):
        years_since_start = (date_ts - start_date).days / 365.0
        season_angle = 2 * np.pi * (date_ts.dayofyear / 365.0)
        season_factor = 1 + 0.02 * np.sin(season_angle)
        erp = profile['base_erp'] * ((1 + profile['growth_rate']) ** years_since_start)
        erp *= 1 + np.random.normal(0, 0.02)
        erp = max(700, erp)
        erp_val = int(round(erp))
        need_rate = profile['base_need_rate'] * (1 + np.random.normal(0, 0.05))
        need_rate = np.clip(need_rate, 0.08, 0.2)
        need_count = int(max(40, round(erp_val * need_rate)))
        diabetes = np.clip(profile['base_diabetes'] * season_factor * (1 + np.random.normal(0, 0.03)), 0.045, 0.14)
        ckd = np.clip(profile['base_ckd'] * (1 + np.random.normal(0, 0.04)), 0.03, 0.08)
        seifa = np.clip(profile['seifa'] * (1 + np.random.normal(0, 0.02)), 0.05, 0.95)
        income = profile['income_base'] * ((1 + profile['income_growth']) ** years_since_start)
        income *= 1 + np.random.normal(0, 0.015)
        income_val = int(round(income / 500) * 500)
        calvary_sites = int(np.clip(round(profile['calvary_sites_base'] + np.random.normal(0, 0.4)), 0, 7))
        competitor_sites = int(np.clip(round(profile['competitor_sites_base'] + np.random.normal(0, 0.6)), 1, 10))
        rac_beds = int(np.clip(profile['rac_beds_base'] * (0.9 + 0.2 * np.random.rand()) + (calvary_sites + competitor_sites) * 35, 120, 1600))
        travel_noise = 1 + np.random.normal(0, 0.04)
        travel_minutes = np.clip(profile['travel_base'] * travel_noise * (1 + 0.05 * (1 - seifa)), 15, 80)
        erp_scaled = np.clip((erp_val - 600) / 5400, 0, 1)
        assist_rate = need_count / max(erp_val, 1)
        assist_scaled = np.clip(assist_rate / 0.22, 0, 1)
        diabetes_scaled = np.clip((diabetes - 0.045) / 0.085, 0, 1)
        ckd_scaled = np.clip((ckd - 0.03) / 0.05, 0, 1)
        seifa_scaled = np.clip(1 - seifa, 0, 1)
        demand_index = (0.3 * erp_scaled + 0.25 * assist_scaled + 0.2 * diabetes_scaled + 0.15 * ckd_scaled + 0.1 * seifa_scaled) * 100
        service_capacity = calvary_sites * 140 + competitor_sites * 110 + rac_beds * 0.08
        demand_pressure = erp_val * 0.08 + need_count * 0.5
        coverage_ratio = np.clip((service_capacity / max(demand_pressure, 50)) * (0.96 + 0.08 * np.random.rand()), 0.2, 1.9)
        comp_intensity = np.clip(competitor_sites / max(erp_val / 1000, 0.1), 0, 3)
        total_sites = calvary_sites + competitor_sites
        calvary_share = calvary_sites / total_sites if total_sites > 0 else 0.0
        quality_score = np.clip(profile['risk_base'] * (0.95 + 0.1 * np.random.rand()), 35, 85)
        rows.append({
            'sa2_code': profile['sa2_code'],
            'sa2_name': profile['sa2_name'],
            'sa3_name': profile['sa3_name'],
            'state': profile['state'],
            'region_type': profile['region_type'],
            'date': date_ts,
            'erp_65_plus': erp_val,
            'need_for_assistance_no': need_count,
            'diabetes_percent': float(diabetes),
            'ckd_percent': float(ckd),
            'seifa_irsd_percentile': float(seifa),
            'median_equivalised_household_income': income_val,
            'calvary_site_count_30min': calvary_sites,
            'competitor_site_count_30min': competitor_sites,
            'rac_beds_within_30min': rac_beds,
            'travel_minutes_per_visit': float(travel_minutes),
            'demand_index': float(np.clip(demand_index, 0, 100)),
            'coverage_ratio': float(coverage_ratio),
            'competitive_intensity_index': float(comp_intensity),
            'calvary_site_share': float(calvary_share),
            'quality_compliance_risk_score': float(quality_score)
        })

df = pd.DataFrame(rows)
assert len(df) == 150000, f"Row count mismatch: {len(df)}"

channel_options = ['GP Referral', 'My Aged Care', 'Web', 'Phone']
channel_probs = [0.35, 0.25, 0.25, 0.15]
df['channel'] = np.random.choice(channel_options, size=len(df), p=channel_probs)

service_line_options = ['Connected Care', 'Home Care', 'RAC', 'Hospital in the Home']
service_line_probs = [0.6, 0.2, 0.15, 0.05]
df['service_line'] = np.random.choice(service_line_options, size=len(df), p=service_line_probs)

platform_options = ['Salesforce', 'Web Portal', 'Phone']
platform_probs = [0.55, 0.25, 0.20]
df['platform'] = np.random.choice(platform_options, size=len(df), p=platform_probs)

device_options = ['Mobile', 'Desktop', 'Tablet']
device_probs = [0.65, 0.30, 0.05]
df['device_type'] = np.random.choice(device_options, size=len(df), p=device_probs)

assist_ratio = df['need_for_assistance_no'] / df['erp_65_plus'].clip(lower=1)
segment_age_band = np.full(len(df), '65-74', dtype=object)
mid_mask = (assist_ratio >= 0.12) | (df['erp_65_plus'] > 3200)
segment_age_band[mid_mask] = '75-84'
older_mask = (assist_ratio >= 0.17) | (df['erp_65_plus'] > 5000)
segment_age_band[older_mask] = '85+'
df['segment_age_band'] = segment_age_band

vulnerability = np.full(len(df), 'Mixed', dtype=object)
low_income_mask = (df['median_equivalised_household_income'] < 65000) | (df['seifa_irsd_percentile'] < 0.3)
vulnerability[low_income_mask] = 'Low Income'
high_chronic_mask = (df['diabetes_percent'] >= 0.09) | (df['ckd_percent'] >= 0.055)
vulnerability[high_chronic_mask] = 'High Chronic'
high_disability_mask = assist_ratio > 0.16
vulnerability[high_disability_mask] = 'High Disability'
df['vulnerability_segment'] = vulnerability

if SCENARIO_CONFIG['enable_performance_spike']:
    spike_mask = (df['date'] >= spike_start_date) & (df[SCENARIO_CONFIG['affected_segment_type']] == SCENARIO_CONFIG['affected_segment'])
    if spike_mask.any():
        spike_multiplier = np.random.uniform(SCENARIO_CONFIG['spike_magnitude'] * 0.9,
                                             SCENARIO_CONFIG['spike_magnitude'] * 1.1,
                                             size=spike_mask.sum())
        df.loc[spike_mask, SCENARIO_CONFIG['spike_metric']] = np.clip(
            df.loc[spike_mask, SCENARIO_CONFIG['spike_metric']] * spike_multiplier,
            0,
            100
        )

if SCENARIO_CONFIG['enable_degradation']:
    degradation_mask = (
        (df['date'] >= degradation_start_date) &
        (df[SCENARIO_CONFIG['degradation_dimension']] == SCENARIO_CONFIG['degradation_segment'])
    )
    if degradation_mask.any():
        df.loc[degradation_mask, SCENARIO_CONFIG['degradation_metric']] = (
            df.loc[degradation_mask, SCENARIO_CONFIG['degradation_metric']]
            * (1 - SCENARIO_CONFIG['degradation_magnitude'])
        )
        df.loc[degradation_mask, SCENARIO_CONFIG['degradation_metric']] = df.loc[degradation_mask, SCENARIO_CONFIG['degradation_metric']].clip(lower=0.15)

if SCENARIO_CONFIG['enable_anomaly']:
    anomaly_mask = df[SCENARIO_CONFIG['anomaly_dimension']] == SCENARIO_CONFIG['anomaly_segment']
    if anomaly_mask.any():
        anomaly_boost = np.random.uniform(
            1 + SCENARIO_CONFIG['anomaly_variance'] * 0.9,
            1 + SCENARIO_CONFIG['anomaly_variance'] * 1.1,
            size=anomaly_mask.sum()
        )
        df.loc[anomaly_mask, SCENARIO_CONFIG['anomaly_metric']] = np.clip(
            df.loc[anomaly_mask, SCENARIO_CONFIG['anomaly_metric']] * anomaly_boost,
            15,
            95
        )

df['addressable_65_plus'] = 0
coverage_gap_mask = df['coverage_ratio'] < 0.6
df.loc[coverage_gap_mask, 'addressable_65_plus'] = df.loc[coverage_gap_mask, 'erp_65_plus']

df['underserved_flag'] = (df['demand_index'] >= 70) & (df['coverage_ratio'] < 0.6)

capacity_component = (
    df['calvary_site_count_30min'] * 95 +
    df['competitor_site_count_30min'] * 45 +
    df['rac_beds_within_30min'] * 0.04
)
travel_factor = (1.1 - (df['travel_minutes_per_visit'] / 130)).clip(lower=0.25, upper=1.15)
demand_component = df['need_for_assistance_no'] * 0.12
df['est_connected_care_visits_week'] = np.clip((capacity_component * travel_factor) + demand_component, 20, 650)

roi_base = (
    0.95 +
    0.25 * (df['platform'] == 'Salesforce').astype(float) +
    0.1 * (df['channel'] == 'Web').astype(float) +
    0.05 * df['state'].isin(['NSW', 'VIC', 'QLD']).astype(float) -
    0.05 * (df['device_type'] == 'Desktop').astype(float)
)
roi_noise = np.random.normal(1, 0.05, len(df))
df['roi_index'] = np.clip(roi_base * roi_noise, 0.85, 1.9)

df['week_start'] = df['date'] - pd.to_timedelta(df['date'].dt.weekday, unit='D')
df['month_start'] = df['date'].dt.to_period('M').dt.start_time
df['quarter'] = df['date'].dt.year.astype(str) + '-Q' + df['date'].dt.quarter.astype(str)
df['year'] = df['date'].dt.year.astype(int)

as_of_timestamp = pd.Timestamp(datetime(2025, 11, 16, 4, 0, 0))
df['as_of'] = as_of_timestamp

df['row_id'] = [str(uuid.uuid4()) for _ in range(len(df))]

df = df[
    [
        'row_id', 'as_of', 'date', 'week_start', 'month_start', 'quarter', 'year',
        'sa2_code', 'sa2_name', 'sa3_name', 'state',
        'channel', 'service_line', 'segment_age_band', 'vulnerability_segment',
        'platform', 'device_type',
        'erp_65_plus', 'need_for_assistance_no', 'diabetes_percent', 'ckd_percent',
        'seifa_irsd_percentile', 'median_equivalised_household_income',
        'calvary_site_count_30min', 'competitor_site_count_30min', 'rac_beds_within_30min',
        'demand_index', 'coverage_ratio', 'addressable_65_plus',
        'competitive_intensity_index', 'calvary_site_share',
        'est_connected_care_visits_week', 'travel_minutes_per_visit',
        'roi_index', 'quality_compliance_risk_score', 'underserved_flag'
    ]
]

recent_pct = (df['date'] >= recent_6mo_date).mean()
date_range_days = (df['date'].max() - df['date'].min()).days
assert date_range_days >= 728, f"Date range too short: {date_range_days}"
assert recent_pct >= 0.55, f"Recent distribution too low: {recent_pct:.2%}"

if SCENARIO_CONFIG['enable_performance_spike']:
    spike_data = df[df['date'] >= spike_start_date]
    spike_segment = spike_data[spike_data[SCENARIO_CONFIG['affected_segment_type']] == SCENARIO_CONFIG['affected_segment']]
    baseline_window_start = spike_start_date - timedelta(days=180)
    baseline_data = df[(df['date'] >= baseline_window_start) & (df['date'] < spike_start_date)]
    baseline_segment = baseline_data[baseline_data[SCENARIO_CONFIG['affected_segment_type']] == SCENARIO_CONFIG['affected_segment']]
    spike_mean = spike_segment[SCENARIO_CONFIG['spike_metric']].mean()
    baseline_mean = baseline_segment[SCENARIO_CONFIG['spike_metric']].mean()
    spike_ratio = spike_mean / baseline_mean if baseline_mean > 0 else 0
    assert spike_ratio >= 2.0, f"Spike ratio too low: {spike_ratio:.2f}"

if SCENARIO_CONFIG['enable_degradation']:
    degradation_recent = df[(df['date'] >= degradation_start_date) & (df[SCENARIO_CONFIG['degradation_dimension']] == SCENARIO_CONFIG['degradation_segment'])]
    degradation_baseline = df[(df['date'] < degradation_start_date) & (df[SCENARIO_CONFIG['degradation_dimension']] == SCENARIO_CONFIG['degradation_segment'])]
    if len(degradation_recent) > 0 and len(degradation_baseline) > 0:
        recent_mean = degradation_recent[SCENARIO_CONFIG['degradation_metric']].mean()
        baseline_mean = degradation_baseline[SCENARIO_CONFIG['degradation_metric']].mean()
        degradation_change = (baseline_mean - recent_mean) / baseline_mean if baseline_mean > 0 else 0
        assert degradation_change >= 0.15, f"Degradation change too small: {degradation_change:.2%}"

if SCENARIO_CONFIG['enable_anomaly']:
    anomaly_segment_mean = df[df[SCENARIO_CONFIG['anomaly_dimension']] == SCENARIO_CONFIG['anomaly_segment']][SCENARIO_CONFIG['anomaly_metric']].mean()
    non_anomaly_mean = df[df[SCENARIO_CONFIG['anomaly_dimension']] != SCENARIO_CONFIG['anomaly_segment']][SCENARIO_CONFIG['anomaly_metric']].mean()
    anomaly_variance = (anomaly_segment_mean - non_anomaly_mean) / non_anomaly_mean if non_anomaly_mean > 0 else 0
    assert anomaly_variance >= 0.35, f"Anomaly variance too low: {anomaly_variance:.2%}"

csv_filename = 'f_service_demand_flat.csv'
hyper_filename = 'f_service_demand_flat.hyper'

export_df = df.copy()
date_columns = ['date', 'week_start', 'month_start']
for col in date_columns:
    export_df[col] = pd.to_datetime(export_df[col]).dt.strftime('%d/%m/%Y')
export_df['as_of'] = pd.to_datetime(export_df['as_of'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S %Z')
export_df.to_csv(csv_filename, index=False)

ensure_package('pantab')
ensure_package('pyarrow')
import pantab  # noqa: E402

hyper_df = df.copy()
timestamp_cols = ['date', 'week_start', 'month_start', 'as_of']
for col in timestamp_cols:
    hyper_df[col] = pd.to_datetime(hyper_df[col])
string_cols = ['row_id', 'sa2_code', 'sa2_name', 'sa3_name', 'state', 'channel', 'service_line',
               'segment_age_band', 'vulnerability_segment', 'platform', 'device_type', 'quarter']
for col in string_cols:
    hyper_df[col] = hyper_df[col].astype(str)
int_cols = ['erp_65_plus', 'need_for_assistance_no', 'median_equivalised_household_income',
            'calvary_site_count_30min', 'competitor_site_count_30min', 'rac_beds_within_30min',
            'addressable_65_plus', 'year']
for col in int_cols:
    hyper_df[col] = hyper_df[col].astype('int64')
hyper_df['underserved_flag'] = hyper_df['underserved_flag'].astype(bool)

pantab.frame_to_hyper(hyper_df, hyper_filename, table='Extract')

print("✅ Data generation complete")
print(f"Total rows: {len(df)}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Recent 6-month share: {recent_pct:.2%}")
print(f"CSV exported to {csv_filename}")
print(f"Hyper exported to {hyper_filename}")
print("Executive Summary:", EXECUTIVE_SUMMARY)
