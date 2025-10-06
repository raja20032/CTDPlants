# Create the main Streamlit application
app_code = '''import streamlit as st
import json
import math
from typing import List, Dict

# Configure the page
st.set_page_config(
    page_title="Garden Paradise - Plant Shop",
    page_icon="🌱",
    layout="wide"
)

# Load data functions
@st.cache_data
def load_plants_data():
    with open('plants_data.json', 'r') as f:
        return json.load(f)

@st.cache_data
def load_coupons_data():
    with open('coupons.json', 'r') as f:
        return json.load(f)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'page' not in st.session_state:
    st.session_state.page = 'main'

def add_to_cart(plant_id: int, plant_name: str, plant_price: float):
    """Add a plant to the cart"""
    if plant_id in st.session_state.cart:
        st.session_state.cart[plant_id]['quantity'] += 1
    else:
        st.session_state.cart[plant_id] = {
            'name': plant_name,
            'price': plant_price,
            'quantity': 1
        }
    st.success(f"Added {plant_name} to cart!")

def remove_from_cart(plant_id: int):
    """Remove a plant from the cart"""
    if plant_id in st.session_state.cart:
        del st.session_state.cart[plant_id]
        st.rerun()

def update_quantity(plant_id: int, new_quantity: int):
    """Update quantity of a plant in cart"""
    if new_quantity <= 0:
        remove_from_cart(plant_id)
    else:
        st.session_state.cart[plant_id]['quantity'] = new_quantity

def calculate_total():
    """Calculate total cart value"""
    total = 0
    for item in st.session_state.cart.values():
        total += item['price'] * item['quantity']
    return total

def apply_coupon(coupon_code: str, total: float):
    """Apply coupon discount"""
    coupons = load_coupons_data()
    if coupon_code.upper() in coupons['coupons']:
        discount_percent = coupons['coupons'][coupon_code.upper()]['discount_percent']
        discount_amount = total * (discount_percent / 100)
        return discount_amount, discount_percent
    return 0, 0

def filter_plants(plants: List[Dict], size_filter: List[str], color_filter: List[str]):
    """Filter plants based on size and color"""
    filtered = []
    for plant in plants:
        size_match = not size_filter or plant['size'] in size_filter
        color_match = not color_filter or plant['color'] in color_filter
        if size_match and color_match:
            filtered.append(plant)
    return filtered

def display_plant_card(plant: Dict):
    """Display a single plant card"""
    with st.container():
        st.image(plant['image'], width=200)
        st.subheader(plant['name'])
        st.write(plant['description'])
        st.write(f"**${plant['price']:.2f}**")
        
        # Add size and color badges
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Size: {plant['size'].title()}")
        with col2:
            st.caption(f"Color: {plant['color'].title()}")
        
        if st.button(f"Add to Cart", key=f"add_{plant['id']}", use_container_width=True):
            add_to_cart(plant['id'], plant['name'], plant['price'])

def show_main_page():
    """Display the main shopping page"""
    st.title("🌱 Garden Paradise - Plant Shop")
    st.markdown("*Beautiful plants anyone can grow outdoors*")
    
    # Load plants data
    plants_data = load_plants_data()
    plants = plants_data['plants']
    
    # Create sidebar for filters
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Size filter
        st.subheader("Plant Size")
        size_options = ['small', 'medium', 'big']
        selected_sizes = []
        for size in size_options:
            if st.checkbox(size.title(), key=f"size_{size}"):
                selected_sizes.append(size)
        
        # Color filter
        st.subheader("Plant Color")
        color_options = list(set([plant['color'] for plant in plants]))
        color_options.sort()
        selected_colors = []
        for color in color_options:
            if st.checkbox(color.title(), key=f"color_{color}"):
                selected_colors.append(color)
        
        # Cart summary
        st.divider()
        cart_count = sum(item['quantity'] for item in st.session_state.cart.values())
        st.metric("🛒 Items in Cart", cart_count)
        
        if st.button("View Cart", use_container_width=True):
            st.session_state.page = 'cart'
            st.rerun()
    
    # Filter plants
    filtered_plants = filter_plants(plants, selected_sizes, selected_colors)
    
    if not filtered_plants:
        st.warning("No plants match your current filters. Try adjusting your selection.")
        return
    
    # Display plants in rows of 4
    plants_per_row = 4
    num_rows = math.ceil(len(filtered_plants) / plants_per_row)
    
    for row in range(num_rows):
        cols = st.columns(plants_per_row)
        for col_idx in range(plants_per_row):
            plant_idx = row * plants_per_row + col_idx
            if plant_idx < len(filtered_plants):
                with cols[col_idx]:
                    display_plant_card(filtered_plants[plant_idx])

def show_cart_page():
    """Display the cart page"""
    st.title("🛒 Your Shopping Cart")
    
    if st.button("← Back to Shop"):
        st.session_state.page = 'main'
        st.rerun()
    
    if not st.session_state.cart:
        st.info("Your cart is empty! Go back to the shop to add some plants.")
        return
    
    # Display cart items
    st.subheader("Cart Items")
    
    # Create a container for cart items
    for plant_id, item in st.session_state.cart.items():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['name']}**")
            
            with col2:
                st.write(f"${item['price']:.2f}")
            
            with col3:
                # Quantity selector
                new_quantity = st.number_input(
                    "Qty", 
                    min_value=1, 
                    value=item['quantity'], 
                    key=f"qty_{plant_id}",
                    label_visibility="collapsed"
                )
                if new_quantity != item['quantity']:
                    update_quantity(plant_id, new_quantity)
                    st.rerun()
            
            with col4:
                subtotal = item['price'] * item['quantity']
                st.write(f"${subtotal:.2f}")
            
            with col5:
                if st.button("Remove", key=f"remove_{plant_id}"):
                    remove_from_cart(plant_id)
        
        st.divider()
    
    # Calculate totals
    subtotal = calculate_total()
    
    # Coupon section
    st.subheader("💰 Coupon Code")
    coupon_col1, coupon_col2 = st.columns([3, 1])
    
    with coupon_col1:
        coupon_code = st.text_input("Enter coupon code:", placeholder="e.g., WELCOME10")
    
    discount_amount = 0
    discount_percent = 0
    
    if coupon_code:
        discount_amount, discount_percent = apply_coupon(coupon_code, subtotal)
        if discount_amount > 0:
            st.success(f"Coupon applied! You saved {discount_percent}% (${discount_amount:.2f})")
        else:
            st.error("Invalid coupon code")
    
    # Order summary
    st.subheader("📋 Order Summary")
    
    summary_col1, summary_col2 = st.columns([2, 1])
    with summary_col1:
        st.write("Subtotal:")
        if discount_amount > 0:
            st.write(f"Discount ({discount_percent}%):")
            st.write("**Total:**")
        else:
            st.write("**Total:**")
    
    with summary_col2:
        st.write(f"${subtotal:.2f}")
        if discount_amount > 0:
            st.write(f"-${discount_amount:.2f}")
            final_total = subtotal - discount_amount
            st.write(f"**${final_total:.2f}**")
        else:
            st.write(f"**${subtotal:.2f}**")
    
    # Checkout button
    st.divider()
    if st.button("🚀 Proceed to Checkout", use_container_width=True, type="primary"):
        st.balloons()
        st.success("Thank you for your order! Your plants will be delivered soon! 🌱")
        st.session_state.cart = {}  # Clear cart after checkout

# Main app logic
def main():
    # Navigation
    if st.session_state.page == 'main':
        show_main_page()
    elif st.session_state.page == 'cart':
        show_cart_page()

if __name__ == "__main__":
    main()
'''

# Save the main application file
with open('app.py', 'w') as f:
    f.write(app_code)

print("Created app.py - Main Streamlit application")