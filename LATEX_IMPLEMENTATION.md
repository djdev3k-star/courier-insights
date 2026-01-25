# LaTeX Formatting in Streamlit - Exploration Results

## Status: ✅ FULLY SUPPORTED

Streamlit 1.53+ (current version) has native LaTeX support via KaTeX rendering engine.

## Implementation Methods

### 1. Block-Level Math: `st.latex()`
```python
st.latex(r"""
\text{Efficiency} = \frac{\text{Total Earnings}}{\text{Total Miles}}
""")
```
- Centered, display-mode math
- Perfect for prominent formulas
- Requires raw string (`r"..."`)

### 2. Inline Math in Markdown: `$...$` and `$$...$$`
```python
st.markdown(r"""
Your efficiency is $\frac{earnings}{miles}$ per mile.

### Block equation:
$$\eta = \frac{E}{M}$$
""")
```
- Inline uses single dollars: `$...$`
- Block uses double dollars: `$$...$$`
- Works in st.markdown() calls
- Requires escaping: `\\` for backslash

### 3. Plotly Integration
```python
fig.update_layout(
    title="Efficiency: $\\eta = \\frac{E}{M}$",
    yaxis_title="$\\eta$ ($/mile)"
)
```
- LaTeX in chart titles/labels
- Double backslashes in Python strings

## Practical Applications for Courier App

### Use Cases:
1. **Efficiency Metrics Section** - Display formulas for how metrics are calculated
2. **Strategic Recommendations** - Show math behind 20% growth targets
3. **Financial Analysis** - Present earning/cost/profit calculations
4. **Trend Analysis** - Label charts with mathematical expressions
5. **Year-End Report** - Professional presentation of KPIs with formulas

### Examples:

**Efficiency Benchmark:**
$$\eta_{\text{current}} = \frac{\$2,100}{750\text{ mi}} = \$2.80/\text{mile}$$

**20% Growth Target:**
$$\eta_{\text{target}} = \eta_{\text{current}} \times 1.20 = \$3.36/\text{mile}$$

**Monthly Earnings:**
$$E_{\text{monthly}} = \sum_{i=1}^{n} (\text{Trip}_i \text{ Earnings})$$

**Reimbursement Impact:**
$$\text{Net Earnings} = \text{Gross} - \text{Shop \& Pay Reimbursements}$$

## Technical Details

### What Works ✅
- All standard LaTeX math commands
- Greek letters: `\alpha, \beta, \eta, \sigma, etc.`
- Fractions, sums, integrals
- Subscripts/superscripts: `x_i`, `x^2`
- Text in math: `\text{...}`
- Multi-line equations with `\begin{align}...\end{align}`

### Limitations ⚠️
- **KaTeX** rendering (not full LaTeX)
- No custom packages/macros
- Limited to math expressions
- Cannot use document structure commands
- Should use raw strings to avoid escape issues

## Implementation Strategy

### Phase 1 (Low Risk): Add to Year-End Report
- Replace text descriptions with LaTeX formulas
- Examples: efficiency calculations, growth targets
- Use `st.latex()` for prominent metrics
- Use `$...$` in markdown context for inline

### Phase 2 (Medium): Enhance Metrics Pages
- Add formula explanations to sidebar metrics
- Label charts with LaTeX expressions
- Show calculation context for KPIs

### Phase 3 (Advanced): Interactive Calculations
- Create tabs showing "how we calculated X"
- Use KaTeX to display formula, then values
- Help users understand metric derivations

## File Structure

```
courier/
├── courier_insights.py          (main app - can add LaTeX here)
├── latex_exploration.py         (test/demo file - shows all features)
└── LATEX_IMPLEMENTATION.md      (this file - reference guide)
```

## Example Code Snippets Ready to Use

### 1. Efficiency Dashboard Card
```python
st.markdown("""
### Efficiency Metric
Your operation runs at: $\\eta = \\${}\\text{/mile}$

To achieve 20% growth:
$$\\eta_{\\text{target}} = \\eta_{\\text{current}} \\times 1.20 = \\${} \\text{/mile}$$
""".format(current_efficiency, target_efficiency))
```

### 2. Monthly Summary with Formulas
```python
st.markdown(f"""
Monthly Performance:

$$E = \\frac{{\\text{{Total Earnings}}}}{{\\text{{Trip Count}}}} = \\frac{{${total:.2f}}}{{${trips}}} = ${avg:.2f}/\\text{{trip}}$$

$$\\eta = \\frac{{\\text{{Net Earnings}}}}{{\\text{{Miles}}}} = \\frac{{${net:.2f}}}{{${miles}}} = ${efficiency:.2f}/\\text{{mile}}$$
""")
```

### 3. Trend Chart with Math Labels
```python
fig.add_annotation(
    x=months[0], y=efficiency_trend[0],
    text=r"$\eta = \frac{\text{Earnings}}{\text{Miles}}$",
    showarrow=True,
    font=dict(size=12)
)
```

## Recommendation

**✅ YES - Implement LaTeX Formatting**

The courier app would benefit significantly from LaTeX:
- Makes complex calculations transparent and professional
- Helps users understand optimization metrics
- Improves credibility of Year-End Report
- Low implementation cost (simple text changes)
- No additional dependencies needed (KaTeX built into Streamlit)

**Start with:** Year-End Report Operational Efficiency section
**Then expand to:** Restaurant efficiency, route optimization calculations, and trend analysis labels

---

**Created:** 2026-01-25 | **Branch:** `feature/latex-formatting`
