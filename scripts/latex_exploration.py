"""
LaTeX Formatting Exploration for Streamlit
Streamlit 1.53+ supports LaTeX rendering via st.latex() and inline LaTeX in markdown
"""
import streamlit as st

st.set_page_config(page_title="LaTeX Exploration", layout="wide")

st.title("LaTeX Formatting in Streamlit")

st.header("1. Using st.latex() - Block Math")
st.write("Display centered, block-level mathematical expressions:")

st.latex(r"""
\text{Efficiency Ratio} = \frac{\text{Total Earnings}}{\text{Total Miles Driven}}
""")

st.latex(r"""
E = mc^2
""")

st.latex(r"""
\text{Monthly Earnings} = \sum_{i=1}^{n} (\text{Trip}_i \text{ Earnings})
""")

st.header("2. Inline LaTeX in Markdown (with KaTeX)")
st.write("Streamlit 1.53+ supports inline LaTeX wrapped in `$...$` within markdown:")

st.markdown("""
Your efficiency metric is $\\frac{\\text{earnings}}{\\text{miles}}$ per mile driven. 
If you earn $500 over 200 miles, your efficiency is $\\frac{500}{200} = 2.50$ dollars per mile.

### Key Formulas:

- **Average Per Trip**: $\\bar{x}_{trip} = \\frac{\\sum_{i=1}^{n} \\text{earnings}_i}{n}$
- **Efficiency**: $\\eta = \\frac{\\text{total\\_earnings}}{\\text{total\\_miles}}$
- **Monthly Growth**: $\\text{growth} = \\frac{\\text{current\\_month} - \\text{prior\\_month}}{\\text{prior\\_month}} \\times 100\\%$
""")

st.header("3. Plotly Integration with LaTeX")
st.write("Plotly charts also support LaTeX in titles, labels, and annotations:")

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Sample data
months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec']
earnings = [1200, 1450, 1680, 1920, 2100]
miles = [450, 520, 610, 680, 750]
efficiency = [e/m for e, m in zip(earnings, miles)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=months, y=efficiency,
    mode='lines+markers',
    name='$\\eta$ (earnings/mile)',
    line=dict(color='#1e5a96', width=3)
))

fig.update_layout(
    title="Monthly Efficiency Trend: $\\eta = \\frac{\\text{Earnings}}{\\text{Miles}}$",
    xaxis_title="Month",
    yaxis_title="Efficiency ($\\eta$ per mile)",
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.header("4. Multi-line LaTeX (Aligned Equations)")
st.markdown("""
### Compound Efficiency Calculation:

$$\\begin{align}
\\text{Gross Earnings} &= \\sum \\text{trip\\_payouts} \\\\
\\text{Reimbursements} &= \\text{Shop \\& Pay expenses} \\\\
\\text{Net Earnings} &= \\text{Gross Earnings} - \\text{Reimbursements} \\\\
\\text{Efficiency} &= \\frac{\\text{Net Earnings}}{\\text{Miles Driven}}
\\end{align}$$

This framework lets us understand how operational costs impact true profitability.
""")

st.header("5. Limitations & Notes")
st.info("""
✅ **What Works:**
- `st.latex(r"...")` for block math
- `$...$` for inline math in st.markdown()
- `$$...$$` for block math in st.markdown()
- Plotly chart labels/titles with LaTeX syntax
- Most standard LaTeX commands (\\frac, \\sum, \\alpha, etc.)

⚠️ **Limitations:**
- Streamlit uses **KaTeX** for rendering (not full LaTeX)
- Complex LaTeX packages not supported
- Requires raw strings (r"...") or double backslashes (\\\\)
- Limited to mathematical expressions (no document structure like \\chapter)
- Image rendering relies on proper encoding

🎯 **Best For:**
- Efficiency metrics and financial ratios
- Comparing earnings formulas
- Showing statistical calculations
- Professional reporting of metrics
""")

st.header("6. Practical Example for Courier App")
st.markdown("""
### Your Performance Summary

**Monthly Efficiency Metrics:**

$$\\eta_{\\text{current}} = \\frac{\\text{Total Earnings}}{\\text{Total Miles}} = \\frac{\\$2,100}{750\\ \\text{mi}} = \\$2.80/\\text{mile}$$

**Target Growth (20%):**

$$\\eta_{\\text{target}} = \\eta_{\\text{current}} \\times 1.20 = \\$2.80 \\times 1.20 = \\$3.36/\\text{mile}$$

**Growth Required:**

$$\\Delta = \\eta_{\\text{target}} - \\eta_{\\text{current}} = \\$3.36 - \\$2.80 = \\$0.56/\\text{mile}$$

This means optimizing your routes to increase earnings per mile driven by $0.56 to reach your 20% efficiency improvement goal.
""")

st.success("✅ LaTeX formatting is fully supported in Streamlit 1.53+!")
