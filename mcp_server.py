#!/usr/bin/env python3
import json
import sys
from client import KlaviyoPredictiveCLVOmnichannelJourneyTrigger

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        trigger = KlaviyoPredictiveCLVOmnichannelJourneyTrigger()
        cust = {"customer_id": "C-1209", "total_orders": 5, "total_spend_usd": 450.0, "days_since_last_order": 95, "days_since_last_touchpoint": 7}
        res = trigger.evaluate_customer_journey(cust)
        assert res["verdict"] == "JOURNEY_TRIGGERED_SUCCESSFULLY"
        assert res["predictive_metrics"]["churn_probability"] > 0.5
        print(f"[TEST PASS] Klaviyo Journey Trigger Passed! Flow: {res['automated_journey_trigger']['flow_name']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-klaviyo-trigger", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_customer_journey", "description": "Predictive CLV and omnichannel journey trigger"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                trigger = KlaviyoPredictiveCLVOmnichannelJourneyTrigger()
                out = trigger.evaluate_customer_journey(args.get("customer_profile", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
