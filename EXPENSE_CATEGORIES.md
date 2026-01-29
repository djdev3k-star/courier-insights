# Expense Category Classification

**Based on:** Legacy analysis from EXPENSE_REPORT.md and SPENDING_BREAKDOWN_SUMMARY.md

---

## Category Breakdown

### 1. Business Expenses (Tax Deductible)
**Total: $858.01** (based on legacy reports)

- **EV Charging**: $241.10 - Vehicle operating costs for delivery operations
- **Vehicle Fuel**: $528.24 - Gas station purchases for vehicle operation
- **Phone/Internet**: $88.67 - Communication services for deliveries

**Tax Status**: Fully deductible business expenses
**Accounting Treatment**: Operating expenses, reduce taxable income

---

### 2. Customer Purchases (Reimbursable)
**Total: $4,815.68**

- Restaurant/food purchases made on behalf of customers
- Matched to trip completion times (±2 hour window)
- Should be tracked for reimbursement from Uber/customers

**Tax Status**: Not deductible (reimbursed by customers)
**Accounting Treatment**: Accounts receivable, not true expenses

---

### 3. Personal Spending (Owner Withdrawals)
**Total: $3,528.17**

Categories include:
- Restaurant dining (personal meals)
- Fast food (personal consumption)
- Groceries & household supplies
- Health & wellness
- Convenience store purchases
- Entertainment & recreation

**Tax Status**: Not deductible
**Accounting Treatment**: Owner withdrawals/distributions, not business expenses

---

## Report Updates

The LaTeX reports now separate these categories:

1. **Master Summary Report**: Shows business profit after expenses, then subtracts personal withdrawals
2. **Business Expenses Report**: Only tax-deductible business costs
3. **Complete Expense Report**: All expenses color-coded by category
4. **Monthly Performance Report**: Month-by-month earnings and expense breakdown

---

## Database Schema

Expenses table now includes:
- `category`: business, personal, customer_purchase, other
- `subcategory`: Detailed classification
- `is_reimbursable`: Boolean flag for customer purchases
- `is_tax_deductible`: Boolean flag for business expenses

---

## Key Insight

**81.9% of spending is personal/customer-related, not true business expenses.**

Only $858.01 represents legitimate business operating costs that reduce taxable income.
