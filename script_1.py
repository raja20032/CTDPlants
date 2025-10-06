# Create the coupon codes JSON file
coupons_data = {
    "coupons": {
        "WELCOME10": {
            "discount_percent": 10,
            "description": "Welcome discount - 10% off"
        },
        "SPRING20": {
            "discount_percent": 20,
            "description": "Spring special - 20% off"
        },
        "SAVE5": {
            "discount_percent": 5,
            "description": "Save 5% on your order"
        },
        "GARDEN25": {
            "discount_percent": 25,
            "description": "Garden lover special - 25% off"
        },
        "NEWCUSTOMER": {
            "discount_percent": 15,
            "description": "New customer discount - 15% off"
        }
    }
}

# Save the coupons data
with open('coupons.json', 'w') as f:
    json.dump(coupons_data, f, indent=2)

print("Created coupons.json with", len(coupons_data['coupons']), "coupon codes")
print("Available coupons:")
for code, details in coupons_data['coupons'].items():
    print(f"- {code}: {details['discount_percent']}% off - {details['description']}")