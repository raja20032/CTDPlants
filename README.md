# Garden Paradise - Plant Shop

A simple shopping website built with Python and Streamlit, featuring a beautiful plant theme for outdoor plants.

## Features

- **Main Shopping Page**: Browse plants in a grid layout (4 cards per row)
- **Plant Cards**: Each card shows image, name, description, and price
- **Filtering System**: Filter by plant size (small, medium, big) and colors
- **Shopping Cart**: Add plants to cart with quantity management
- **Coupon System**: Apply discount codes for special offers

## Files Structure

- `app.py` - Main Streamlit application
- `plants_data.json` - Plant inventory data
- `coupons.json` - Coupon codes and discount information
- `requirements.txt` - Python dependencies
- `README.md` - This file

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser to the URL shown (usually `http://localhost:8501`)

## Available Coupon Codes

- `WELCOME10` - 10% off (Welcome discount)
- `SPRING20` - 20% off (Spring special)
- `SAVE5` - 5% off (Save on your order)
- `GARDEN25` - 25% off (Garden lover special)
- `NEWCUSTOMER` - 15% off (New customer discount)

## Customization

### Adding New Plants
Edit `plants_data.json` to add new plants. Each plant should have:
- `id`: unique identifier
- `name`: plant name
- `description`: short description
- `price`: price as a number
- `size`: "small", "medium", or "big"
- `color`: color name
- `image`: URL to plant image

### Adding New Coupons
Edit `coupons.json` to add new coupon codes. Each coupon should have:
- `discount_percent`: percentage discount (0-100)
- `description`: description of the coupon

## Features Included

✅ Main page with plant grid (4 per row)  
✅ Plant cards with image, name, description, price  
✅ Left sidebar filtering (size and color)  
✅ Add to cart functionality  
✅ Cart page with quantity management  
✅ Coupon code system with JSON configuration  
✅ Responsive design  
✅ Session state management  

Enjoy building your plant paradise! 🌱
