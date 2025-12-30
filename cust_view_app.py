import gradio as gr
import pandas as pd
import requests
from supabase import create_client, Client

# --- 1. CONFIGURATION & ASSETS ---
SUPABASE_URL = "https://rrclzngekaxsehdxzniz.supabase.co"
SUPABASE_KEY = "sb_publishable_l1JFx6shu-fea732p5ydjA_Qy7NSmeW"

# Asset URLs
LOGO_URL = "https://github.com/abidsulficar285-hub/mishtee/blob/main/mishtee%20logo.png?raw=true"
STYLE_URL = "https://raw.githubusercontent.com/abidsulficar285-hub/mishtee/refs/heads/main/style.css"

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch Styling
try:
    mishtee_css = requests.get(STYLE_URL).text
except Exception:
    mishtee_css = ".main { font-family: sans-serif; }" # Fallback

# --- 2. LOGIC FUNCTIONS ---

def get_trending_products():
    """Retrieves top 4 best selling products."""
    try:
        # Fetch all orders to calculate popularity
        res = supabase.table("orders").select("product_id, qty_kg").execute()
        if not res.data:
            return pd.DataFrame(columns=["Product", "Total Sold (kg)"])
        
        df = pd.DataFrame(res.data)
        trending = df.groupby("product_id")["qty_kg"].sum().reset_index()
        trending = trending.sort_values(by="qty_kg", ascending=False).head(4)
        
        # Map IDs to Names
        p_ids = trending["product_id"].tolist()
        p_info = supabase.table("products").select("item_id, sweet_name").in_("item_id", p_ids).execute()
        name_map = {p['item_id']: p['sweet_name'] for p in p_info.data}
        
        trending["Product"] = trending["product_id"].map(name_map)
        return trending[["Product", "qty_kg"]].rename(columns={"qty_kg": "Total Sold (kg)"})
    except Exception as e:
        print(f"Trending Error: {e}")
        return pd.DataFrame()

def process_customer_login(phone):
    """Handles greeting, order history, and trending update upon login."""
    if not phone or len(phone) < 10:
        return "⚠️ Please enter a valid phone number.", pd.DataFrame(), get_trending_products()

    # 1. Fetch Name
    c_res = supabase.table("customers").select("full_name").eq("phone", phone).execute()
    if not c_res.data:
        greeting = "Namaste! We couldn't find your profile. Please contact a MishTee hub to register."
        orders_df = pd.DataFrame()
    else:
        name = c_res.data[0]['full_name']
        greeting = f"## Namaste, {name} ji! \n**Great to see you again. [Purity and Health]**"
        
        # 2. Fetch Orders
        o_res = supabase.table("orders").select("order_id, order_date, qty_kg, status").eq("cust_phone", phone).execute()
        orders_df = pd.DataFrame(o_res.data)
        if not orders_df.empty:
            orders_df = orders_df.sort_values("order_date", ascending=False)

    return greeting, orders_df, get_trending_products()

# --- 3. UI LAYOUT (Vertical Stack) ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic Customer Portal") as demo:
    
    # 1. Header Area
    with gr.Column(elem_id="header", variant="compact"):
        gr.Image(LOGO_URL, show_label=False, height=100, width=250, interactive=False, container=False)
        gr.Markdown("<p style='text-align: center; font-style: italic;'>[Purity and Health]</p>")
    
    gr.HTML("<hr>")

    # 2. Welcome/Login Area
    with gr.Row():
        with gr.Column(scale=1):
            phone_input = gr.Textbox(label="Mobile Number", placeholder="98XXXXXXXX", max_lines=1)
            login_btn = gr.Button("Explore My Magic", variant="primary")
        with gr.Column(scale=2):
            greeting_display = gr.Markdown("### Welcome to MishTee-Magic \nEnter your number to view your history and today's trends.")

    # 3. Data Tabs (Sober Minimalist Look)
    with gr.Tabs():
        with gr.TabItem("📦 My Order History"):
            history_table = gr.Dataframe(
                headers=["Order ID", "Date", "Qty (kg)", "Status"],
                interactive=False,
                wrap=True
            )
            
        with gr.TabItem("🔥 Trending Today"):
            trending_table = gr.Dataframe(
                headers=["Product", "Total Sold (kg)"],
                interactive=False
            )
            gr.Markdown("_Updated in real-time from our Ahmedabad Hubs_")

    # Event Mapping
    login_btn.click(
        fn=process_customer_login,
        inputs=phone_input,
        outputs=[greeting_display, history_table, trending_table]
    )

    # Load trending data on page start
    demo.load(fn=get_trending_products, outputs=trending_table)

# --- 4. EXECUTION ---
if __name__ == "__main__":
    demo.launch(debug=True)
