def calculate_risk_score(features):
    """
    Calculate a basic risk score based on input features.

    Args:
        features (list): A list of numerical features.

    Returns:
        float: A risk score between 0 and 1.
    """
    # Simple heuristic: scale and clamp between 0 and 1.
    # features = [subdomain_count, has_valid_ssl (0/1), a_records_count]
    try:
        subdomains = float(features[0]) if len(features) > 0 else 0.0
        ssl_ok = float(features[1]) if len(features) > 1 else 0.0
        a_count = float(features[2]) if len(features) > 2 else 0.0

        # weights tuned for simple prioritization
        score = (
            min(subdomains / 50.0, 1.0) * 0.4 +  # many subdomains → larger surface
            (1.0 - ssl_ok) * 0.4 +               # missing/invalid SSL increases risk
            min(a_count / 10.0, 1.0) * 0.2       # multiple A records implies complexity
        )
        return round(score, 3)
    except Exception as e:
        return f"Error in risk scoring: {str(e)}"
