import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

# Configuration Parameters - Modify these to adjust data characteristics
NUM_ROWS = 150000
OUTLIER_FRACTION = 0.02
OUTLIER_MAGNITUDE = 3.0
RANDOM_SEED = 42

# Set random seeds for reproducibility
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Banking-specific configuration for realistic data generation
SCENARIO_CONFIG = {
    'enable_performance_spike': True,
    'spike_metric': 'CET1_Ratio',
    'spike_period_days': 90,
    'spike_magnitude': 1.15,  # 15% improvement in capital ratios
    'affected_segment': 'Institutional Banking',
    'enable_degradation': True,
    'degradation_dimension': 'Credit_Risk_Category',
    'degradation_duration_months': 6,
    'degradation_magnitude': 0.85,  # 15% degradation
    'outlier_concentration_recent_pct': 80
}

def generate_realistic_business_units(count: int = 15) -> List[str]:
    """Generate realistic banking business unit names"""
    business_units = [
        'Institutional Banking', 'Commercial Banking', 'Retail Banking',
        'Mortgage Services', 'Personal Banking', 'Business Banking', 'Regional Banking',
        'International Banking', 'Investment Banking', 'Wealth Management',
        'Digital Banking', 'Corporate Banking', 'SME Banking', 'Private Banking',
        'Treasury Services', 'Trade Finance', 'Equipment Finance', 'Agricultural Finance'
    ]
    return business_units[:count]

def generate_realistic_regions(count: int = 15) -> List[str]:
    """Generate realistic regional segments"""
    regions = [
        'Metropolitan Area A', 'Metropolitan Area B', 'Metropolitan Area C', 'Metropolitan Area D',
        'Central Business District', 'Regional Center A', 'Regional Center B', 'Regional Center C',
        'Coastal Region A', 'Coastal Region B', 'Northern Region', 'Southern Region',
        'Eastern Region', 'Western Region', 'Rural Region A',
        'Rural Region B', 'Suburban Region A', 'Suburban Region B'
    ]
    return regions[:count]

def generate_credit_risk_categories() -> List[str]:
    """Generate Basel III compliant credit risk categories"""
    return [
        'Low Risk', 'Standard Risk', 'Moderate Risk', 'High Risk',
        'Very High Risk', 'Default Risk', 'Special Mention',
        'Sub-standard', 'Doubtful', 'Loss Category'
    ]

def generate_date_series(start: datetime, end: datetime, size: int) -> pd.Series:
    """Generate date series with realistic distribution weighted toward recent dates"""
    total_days = (end - start).days
    
    # Create weighted distribution favoring recent dates (60% in last 6 months)
    weights = np.linspace(0.1, 2.0, total_days)
    weights = weights / weights.sum()
    
    # Generate random days based on weighted distribution
    random_days = np.random.choice(total_days, size=size, p=weights)
    dates = [start + timedelta(days=int(day)) for day in random_days]
    
    return pd.Series(dates)

def apply_realistic_outliers(series: pd.Series, recent_date_mask: pd.Series, 
                           column_name: str) -> pd.Series:
    """Apply outliers primarily to recent records for specific metrics"""
    if column_name not in ['CET1_Ratio', 'Total_Capital_Ratio', 'Leverage_Ratio', 'RWA_Growth']:
        return series
    
    # Identify recent records (last 20% of date range)
    recent_indices = recent_date_mask[recent_date_mask].index
    
    # Apply outliers to 2% of recent records
    n_outliers = int(len(recent_indices) * OUTLIER_FRACTION)
    if n_outliers == 0:
        return series
        
    outlier_indices = np.random.choice(recent_indices, size=n_outliers, replace=False)
    
    outlier_series = series.copy()
    
    if column_name in ['CET1_Ratio', 'Total_Capital_Ratio', 'Leverage_Ratio']:
        # For capital ratios, create both positive and negative outliers
        half_outliers = max(1, n_outliers//2)
        for idx in outlier_indices[:half_outliers]:
            outlier_series.iloc[idx] *= (1 + np.random.uniform(0.1, 0.3))  # Positive spike
        for idx in outlier_indices[half_outliers:]:
            outlier_series.iloc[idx] *= (1 - np.random.uniform(0.05, 0.15))  # Negative spike
    else:
        # For other metrics, apply standard outlier logic
        outlier_series.iloc[outlier_indices] *= np.random.uniform(2.0, 4.0, len(outlier_indices))
    
    return outlier_series

def inject_scenarios(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Apply story-driven scenarios to baseline data"""
    df_enhanced = df.copy()
    
    # Sort by date to identify time periods
    df_enhanced = df_enhanced.sort_values('Report_Date').reset_index(drop=True)
    
    # Scenario 1: Performance spike in Institutional Banking (last 90 days)
    if config['enable_performance_spike']:
        recent_date = df_enhanced['Report_Date'].max()
        spike_start = recent_date - timedelta(days=config['spike_period_days'])
        
        spike_mask = (
            (df_enhanced['Report_Date'] >= spike_start) & 
            (df_enhanced['Business_Unit'] == config['affected_segment'])
        )
        
        # Apply improvement to capital ratios
        df_enhanced.loc[spike_mask, 'CET1_Ratio'] *= config['spike_magnitude']
        df_enhanced.loc[spike_mask, 'Total_Capital_Ratio'] *= (config['spike_magnitude'] * 0.9)
        df_enhanced.loc[spike_mask, 'RWA_Growth'] *= 0.7  # Lower RWA growth
    
    # Scenario 2: Credit risk degradation in High Risk category
    if config['enable_degradation']:
        degradation_start = df_enhanced['Report_Date'].max() - timedelta(days=config['degradation_duration_months'] * 30)
        
        degradation_mask = (
            (df_enhanced['Report_Date'] >= degradation_start) & 
            (df_enhanced['Credit_Risk_Category'] == 'High Risk')
        )
        
        # Apply degradation to risk metrics - FIXED: Use correct column names
        df_enhanced.loc[degradation_mask, 'Credit_Loss_Provision_Millions'] *= (1 / config['degradation_magnitude'])
        df_enhanced.loc[degradation_mask, 'NPL_Ratio'] *= (1 / config['degradation_magnitude'])
    
    return df_enhanced

def generate_executive_summary(df: pd.DataFrame, config: Dict) -> Dict:
    """Document injected patterns for validation"""
    recent_date = df['Report_Date'].max()
    
    return {
        'primary_insight': f'Institutional Banking CET1 ratio improved by 15% in last {config["spike_period_days"]} days',
        'injected_patterns': [
            'Capital ratio performance spike in Institutional Banking',
            'Credit risk degradation in High Risk category over 6 months',
            'Concentrated outliers in recent reporting periods'
        ],
        'business_impact': 'Capital adequacy ratios exceeded regulatory requirements by 2.5-3.0%',
        'detection_guidance': 'Filter by Business Unit and time period to identify performance anomalies'
    }

def main():
    """Main data generation function"""
    print("Starting Basel III Capital Adequacy data generation...")
    
    # Generate foundational data categories
    business_units = generate_realistic_business_units(15)
    regions = generate_realistic_regions(15)
    credit_risk_categories = generate_credit_risk_categories()
    
    # Generate base date range (3 years of daily reporting)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    print("Generating date series...")
    dates = generate_date_series(start_date, end_date, NUM_ROWS)
    
    # Identify recent date mask for outlier application
    recent_threshold = dates.quantile(0.8)  # Last 20% of date range
    recent_mask = dates >= recent_threshold
    
    print("Generating dimensional data...")
    
    # Generate dimensional attributes
    business_unit = np.random.choice(business_units, NUM_ROWS)
    region = np.random.choice(regions, NUM_ROWS)
    credit_risk_category = np.random.choice(credit_risk_categories, NUM_ROWS)
    
    # Basel III regulatory status
    regulatory_status = np.random.choice(['Compliant', 'Under Review', 'Non-Compliant'], 
                                       NUM_ROWS, p=[0.85, 0.12, 0.03])
    
    print("Generating Basel III capital metrics...")
    
    # Generate Basel III capital adequacy ratios with realistic ranges
    # CET1 Ratio: International banks typically maintain 10-16%
    cet1_base = np.random.normal(12.5, 1.5, NUM_ROWS)
    cet1_ratio = np.clip(cet1_base, 8.0, 18.0)
    
    # Total Capital Ratio: Typically 14-20%
    total_capital_base = cet1_ratio + np.random.normal(3.0, 1.0, NUM_ROWS)
    total_capital_ratio = np.clip(total_capital_base, 10.0, 22.0)
    
    # Leverage Ratio: Basel III minimum 3%, major banks typically 4-7%
    leverage_base = np.random.normal(5.2, 0.8, NUM_ROWS)
    leverage_ratio = np.clip(leverage_base, 3.0, 8.0)
    
    print("Generating risk-weighted assets and provisions...")
    
    # Risk-Weighted Assets (billions USD)
    rwa_base = np.random.lognormal(3.5, 0.8, NUM_ROWS)  # Mean around $30B
    rwa_amount = np.clip(rwa_base, 1.0, 500.0)
    
    # RWA Growth Rate (quarterly)
    rwa_growth = np.random.normal(0.02, 0.05, NUM_ROWS)  # 2% average growth
    
    # Credit Loss Provisions (millions USD)
    credit_loss_base = np.random.exponential(50, NUM_ROWS)
    credit_loss_provision = np.clip(credit_loss_base, 1.0, 2000.0)
    
    # Non-Performing Loans Ratio
    npl_base = np.random.gamma(2, 0.5, NUM_ROWS)
    npl_ratio = np.clip(npl_base, 0.1, 8.0)
    
    # Liquidity Coverage Ratio (Basel III minimum 100%)
    lcr_base = np.random.normal(130, 20, NUM_ROWS)
    lcr_ratio = np.clip(lcr_base, 100.0, 200.0)
    
    print("Applying realistic outliers...")
    
    # Apply outliers to key metrics
    cet1_ratio = apply_realistic_outliers(pd.Series(cet1_ratio), recent_mask, 'CET1_Ratio').values
    total_capital_ratio = apply_realistic_outliers(pd.Series(total_capital_ratio), recent_mask, 'Total_Capital_Ratio').values
    leverage_ratio = apply_realistic_outliers(pd.Series(leverage_ratio), recent_mask, 'Leverage_Ratio').values
    rwa_growth = apply_realistic_outliers(pd.Series(rwa_growth), recent_mask, 'RWA_Growth').values
    
    print("Assembling DataFrame...")
    
    # Create the main DataFrame
    df = pd.DataFrame({
        'Report_Date': dates,
        'Business_Unit': business_unit,
        'Geographic_Region': region,
        'Credit_Risk_Category': credit_risk_category,
        'Regulatory_Status': regulatory_status,
        'CET1_Ratio': np.round(cet1_ratio, 2),
        'Total_Capital_Ratio': np.round(total_capital_ratio, 2),
        'Leverage_Ratio': np.round(leverage_ratio, 2),
        'RWA_Amount_Billions': np.round(rwa_amount, 1),
        'RWA_Growth': np.round(rwa_growth, 4),
        'Credit_Loss_Provision_Millions': np.round(credit_loss_provision, 1),
        'NPL_Ratio': np.round(npl_ratio, 2),
        'LCR_Ratio': np.round(lcr_ratio, 1)
    })
    
    print("Injecting business scenarios...")
    
    # Apply story-driven scenarios
    df_final = inject_scenarios(df, SCENARIO_CONFIG)
    
    # Generate executive summary for validation
    summary = generate_executive_summary(df_final, SCENARIO_CONFIG)
    
    print("Validation and export...")
    
    # Validation checks
    print(f"Generated {len(df_final)} rows")
    print(f"Date range: {df_final['Report_Date'].min()} to {df_final['Report_Date'].max()}")
    print(f"Business Units: {df_final['Business_Unit'].nunique()}")
    print(f"Geographic Regions: {df_final['Geographic_Region'].nunique()}")
    print(f"Average CET1 Ratio: {df_final['CET1_Ratio'].mean():.2f}%")
    print(f"Regulatory Compliance Rate: {(df_final['Regulatory_Status'] == 'Compliant').mean()*100:.1f}%")
    
    # Print executive summary
    print("\n=== EXECUTIVE SUMMARY ===")
    print(f"Primary Insight: {summary['primary_insight']}")
    print(f"Injected Patterns: {', '.join(summary['injected_patterns'])}")
    print(f"Business Impact: {summary['business_impact']}")
    print(f"Detection Guidance: {summary['detection_guidance']}")
    
    # Export to CSV
    output_filename = 'basel_iii_capital_adequacy_data.csv'
    df_final.to_csv(output_filename, index=False)
    print(f"\nData exported to {output_filename}")
    try:
        import pantab
        hyper_filename = f"basel_iii_capital_adequacy_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.hyper"
        pantab.frame_to_hyper(df_final, hyper_filename, table='basel_iii_capital_adequacy_data')
        print(f"Dataset also saved as '{hyper_filename}'")
    except ImportError:
        print("pantab not available - skipping Hyper file generation")
    
    return df_final

# Execute data generation
if __name__ == "__main__":
    generated_data = main()
    print("Data generation completed successfully!")
