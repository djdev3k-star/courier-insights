import re
import time

# Wait a moment for any file handles to release
time.sleep(1)

# Read the file
with open('courier_insights.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all st.plotly_chart calls to add scrollZoom config
content = content.replace(
    'st.plotly_chart(fig, use_container_width=True)',
    "st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})"
)

content = content.replace(
    "st.plotly_chart(fig, width='stretch')",
    "st.plotly_chart(fig, width='stretch', config={'scrollZoom': True})"
)

# Write back
with open('courier_insights.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added scroll zoom to all maps!")
