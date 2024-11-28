import streamlit as st
import streamlit.components.v1 as components

# Embed the HTML content
html_content = """
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
html_content_2=""" 
<creattie-embed
 src="https://d1jj76g3lut4fe.cloudfront.net/saved_colors/106803/k95tFqXIRylINPeF.json"
 delay="1"
 speed="100"
 frame_rate="24"
 trigger="loop"
 style="width:600px;background-color: ">
</creattie-embed>
<script src="https://creattie.com/js/embed.js?id=3f6954fde297cd31b441" defer></script>
"""

html_content_3=""" 
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


# Display the animation
st.title("Creattie Animation in Streamlit")
components.html(html_content_2, height=400)