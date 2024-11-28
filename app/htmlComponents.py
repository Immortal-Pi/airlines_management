import streamlit as st
import streamlit.components.v1 as components

# Embed the HTML content
baggage= """
<creattie-embed
    src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/gdDHBk5EukHPNTSP.json"
    delay="1"
    speed="100"
    frame_rate="24"
    trigger="loop"
    style="width:600px;">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>
"""

transaction=""" 
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/dSRALdaYMXbEEzlO.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>

"""
book_flights=""" 
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/lI0u7cBT3REy1Q61.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>

"""
page_not_found="""
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/uFvbWapqbWW6yZ7x.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>
"""
customer_support=""" 
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/BN2owzjWrk35bDsk.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>
"""

discount=""" 
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/SeLvIyEd7a0uFmZy.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>

"""
# Display the animation
st.title("Creattie Animation in Streamlit")
components.html(customer_support, height=400)