import streamlit as st
import json
import math
from typing import List, Dict

# Configure the page
st.set_page_config(
    page_title="Garden Paradise - Plant Shop",
    page_icon="🌱",
    layout="wide"
)
# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main color scheme */
    :root {
        --primary-green: #2d6a4f;
        --light-green: #52b788;
        --accent-green: #95d5b2;
        --bg-cream: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2d6a4f 0%, #52b788 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Plant card styling */
    .plant-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid #e9ecef;
        height: 100%;
    }
    
    .plant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(45,106,79,0.2);
        border-color: #52b788;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-size {
        background-color: #d3f8e2;
        color: #2d6a4f;
    }
    
    .badge-color {
        background-color: #fff3cd;
        color: #856404;
    }
    
    /* Cart item styling */
    .cart-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #52b788;
    }
    
    /* Summary box */
    .summary-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #52b788;
        margin-top: 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #141414;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background-color: #4d4d4d;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Divider styling */
    hr {
        border-color: #52b788;
        opacity: 0.3;
    }
    
    /* Price styling */
    .price-tag {
        color: #2d6a4f;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* Order card styling */
    .order-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #52b788;
    }
    </style>
""", unsafe_allow_html=True)
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

if 'history' not in st.session_state: #create session state for history to save data
    st.session_state.history = {}

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
    # Set flag to show success message under the corresponding button
    st.session_state.last_added = plant_name
    # cart = { 
    #   plant_id: {
    #       'name': plant_name, 
    #       'price': plant_price, 
    #       'quantity': 1
    #   } 
    #}

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


def calculate_size_discount(plants: List[Dict], subtotal: float):
    """Return automatic size-based discount (amount, percent, label).

    Rules:
    - 3 or more big plants → 20%
    - 4 or more medium plants → 15%
    - 5 or more small plants → 10%

    Chooses the highest eligible discount and applies it to the whole subtotal.
    """
    if not st.session_state.cart:
        return 0.0, 0, ""

    id_to_size = {p['id']: p['size'] for p in plants}
    size_counts = {"big": 0, "medium": 0, "small": 0}

    for plant_id, item in st.session_state.cart.items():
        size = id_to_size.get(plant_id)
        if size in size_counts:
            size_counts[size] += item['quantity']

    candidates = []
    if size_counts["big"] >= 3:
        candidates.append((20, "3 big plants"))
    if size_counts["medium"] >= 4:
        candidates.append((15, "4 medium plants"))
    if size_counts["small"] >= 5:
        candidates.append((10, "5 small plants"))

    if not candidates:
        return 0.0, 0, ""

    best_percent, label = max(candidates, key=lambda t: t[0])
    discount_amount = subtotal * (best_percent / 100)
    return discount_amount, best_percent, label


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

        # Use on_click callback so session_state updates before sidebar re-renders
        st.button(
            "Add to Cart",
            key=f"add_{plant['id']}",
            use_container_width=True,
            on_click=add_to_cart,
            args=(plant['id'], plant['name'], plant['price'])
        )
        if st.session_state.get("last_added") == plant["name"]: # ✅ Show success message right below the button
            st.success(f"Added {plant['name']} to cart!")
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

        elif st.button("Order History", use_container_width=True):
            st.session_state.page = 'history'
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

def show_coupon_page():
    """Coupon Page"""
    st.title("Coupon Page")

    # Load coupon data
    with open('coupons.json', 'r') as f:
        data = json.load(f)
    coupons_data = data["coupons"]

    # Define CSS style for rounded boxes
    st.markdown("""
    <style>
    .rounded-box {
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #E3EEEF;
    }
    .coupon-key {
        font-weight: bold;
        font-size: 22px;
        color: #333333;
        margin-bottom: 10px;
    }
    .coupon-info {
        font-size: 18px;
        color: #070D0D;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render each coupon inside its own rounded box
    for code, details in coupons_data.items():
        st.markdown(f"""
        <div class='rounded-box'>
            <div class='coupon-key'>{code}</div>
            <div class='coupon-info'>Discount: {details['discount_percent']}%</div>
            <div class='coupon-info'>Description: {details['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Cart"):
        st.session_state.page = 'cart'
        st.rerun()

def show_cart_page():
    """Display the cart page"""
    st.title("🛒 Your Shopping Cart")

    if st.button("← Back to Shop"):
        st.session_state.page = 'main'
        st.rerun()
    
    if st.button("View Coupons"):
        st.session_state.page = 'coupon'
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
    total_noGST = calculate_total()

    # Load plants for size lookups and compute automatic size discount
    plants_data = load_plants_data()
    auto_discount_amount, auto_discount_percent, auto_discount_label = calculate_size_discount(plants_data['plants'], total_noGST)

    subtotal_after_auto = total_noGST - auto_discount_amount
    GST_amount = subtotal_after_auto * 0.1
    final_total = subtotal_after_auto + GST_amount


    # Coupon section
    st.subheader("💰 Coupon Code")
    coupon_col1, coupon_col2 = st.columns([3, 1])

    with coupon_col1:
        coupon_code = st.text_input("Enter coupon code:", placeholder="e.g., WELCOME10")

    discount_amount = 0
    discount_percent = 0

    if coupon_code:
        discount_amount, discount_percent = apply_coupon(coupon_code, subtotal_after_auto)
        if discount_amount > 0:
            st.success(f"Coupon applied! You saved {discount_percent}% (${discount_amount:.2f})")
            GST_amount = (subtotal_after_auto - discount_amount) * 0.1  # Apply GST to discounted subtotal
        else:
            st.error("Invalid coupon code")

    # Order summary
    st.subheader("📋 Order Summary")

    summary_col1, summary_col2 = st.columns([2, 1])
    with summary_col1:
        st.write("Subtotal:")
        if auto_discount_amount > 0:
            st.write(f"Auto discount ({auto_discount_percent}% - {auto_discount_label}):")
        if discount_amount > 0:
            st.write(f"Discount ({discount_percent}%):")
        st.write("GST(10%):") #Include GST
        st.write("**Total:**")

    with summary_col2:
        st.write(f"${total_noGST:.2f}") #Subtotal
        if auto_discount_amount > 0:
            st.write(f"-${auto_discount_amount:.2f}")
        if discount_amount > 0:
            st.write(f"-${discount_amount:.2f}")
            final_total = subtotal_after_auto - discount_amount + GST_amount
        st.write(f"${GST_amount:.2f}") #Include GST
        st.write(f"**${final_total:.2f}**")

    # Checkout button
    st.divider()
    if st.button("🚀 Proceed to Checkout", use_container_width=True, type="primary"):
        st.balloons()
        st.success("Thank you for your order! Your plants will be delivered soon! 🌱")
        if st.session_state.history:
            next_key = max(st.session_state.history.keys()) + 1  #Save number of orders
        else:
            next_key = 1
        st.session_state.history[next_key] = {
            "items": st.session_state.cart.copy(), #copy cart, plant_id(name,price,quantity) 
            "subtotal": total_noGST, # original subtotal before discounts
            "GST": GST_amount, # GST after discounts
            "final_total": final_total # final total after all discounts + GST
        }
        total_discount_taken = auto_discount_amount + (discount_amount if discount_amount > 0 else 0)
        if total_discount_taken > 0:
            discount_str = "-$" + str(round(total_discount_taken, 2))
            st.session_state.history[next_key].update({"Discount": discount_str})
        else:
            st.session_state.history[next_key].update({"Discount": "NIL"})
        st.session_state.history[next_key].update({"Coupon": coupon_code if discount_amount > 0 else "NIL"})

        st.session_state.cart = {}  # Clear cart after checkout
def show_history_page(): #Show Order History page
    """Display the history page"""
    st.title("🚚 Your Order History")

    if st.button("← Back to Shop"):
        st.session_state.page = 'main'
        st.rerun()

    if not st.session_state.history:
        st.info("You have not made any orders, Go back to the shop to add some plants.")
        return

    # Display cart items
    st.subheader("Orders made")

    # Create a container for cart items
    for order_id, order_data in st.session_state.history.items():
        st.subheader(f"📦 Order #{order_id}")
        
        # Loop through items inside inner dict this order
        for plant_id, item in order_data["items"].items(): #for each plant_id, run items
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.write(f"**{item['name']}**")

                with col2:
                    st.write(f"${item['price']:.2f}")

                with col3:
                    st.write(f"Qty: {item['quantity']}")

                with col4:
                    subtotal = item['price'] * item['quantity']
                    st.write(f"${subtotal:.2f}")
        st.write(f"Subtotal: ${order_data['subtotal']:.2f}")
        st.write(f"Discounted amount: {order_data['Discount']},   Coupon Code used: {order_data['Coupon']}")
        st.write(f"GST Amount: ${order_data['GST']:.2f}")
        st.write(f"**Final Total: ${order_data['final_total']:.2f}**")
        st.divider()
# Main app logic
def main():
    # Navigation
    if st.session_state.page == 'main':
        show_main_page()
    elif st.session_state.page == 'cart':
        show_cart_page()
    elif st.session_state.page == 'history': #Show Order History page
        show_history_page()
    elif st.session_state.page == 'coupon': #Show Coupon Page
        show_coupon_page()

if __name__ == "__main__":
    main()
