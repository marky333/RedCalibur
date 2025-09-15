from sklearn.ensemble import RandomForestClassifier
import numpy as np

def calculate_risk_score(features):
    """
    Calculate a basic risk score based on input features.

    Args:
        features (list): A list of numerical features.

    Returns:
        float: A risk score between 0 and 1.
    """
    try:
        # Placeholder model for demonstration
        model = RandomForestClassifier()
        model.fit(np.random.rand(10, len(features)), np.random.randint(2, size=10))
        risk_score = model.predict_proba([features])[0][1]
        return risk_score
    except Exception as e:
        return f"Error in risk scoring: {str(e)}"
