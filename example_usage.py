from client import KlaviyoPredictiveCLVOmnichannelJourneyTrigger

def main():
    trigger = KlaviyoPredictiveCLVOmnichannelJourneyTrigger()
    profile = {
        "customer_id": "VIP-8812",
        "total_orders": 8,
        "total_spend_usd": 1280.0,
        "days_since_last_order": 20,
        "days_since_last_touchpoint": 5
    }
    result = trigger.evaluate_customer_journey(profile)
    print("--- Klaviyo Predictive CLV & Journey Trigger ---")
    print(f"Customer: {result['customer_id']} | 365d Predicted CLV: ${result['predictive_metrics']['predicted_next_365d_clv_usd']}")
    print(f"Churn Risk: {result['predictive_metrics']['churn_probability']*100:.1f}%")
    print(f"Flow Triggered: {result['automated_journey_trigger']['flow_name']} via {result['automated_journey_trigger']['channel']}")
    print(f"Incentive: {result['automated_journey_trigger']['incentive_offer']}")

if __name__ == "__main__":
    main()
