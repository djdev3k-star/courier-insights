/*
  # Update Expenses Table with Category Classification
  
  1. Schema Changes
    - Add `category` column (business, personal, customer_purchase, other)
    - Add `is_reimbursable` boolean flag
    - Add `is_tax_deductible` boolean flag
    - Add `subcategory` for detailed classification
  
  2. Data Integrity
    - Default values for backward compatibility
    - Proper indexing for category queries
  
  Based on analysis:
  - Business: EV Charging ($241.10), Vehicle Fuel ($528.24), Phone/Internet ($88.67)
  - Customer Purchases: $4,815.68 (reimbursable)
  - Personal: $3,528.17 (owner withdrawals)
*/

-- Add category columns
ALTER TABLE expenses 
ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'uncategorized',
ADD COLUMN IF NOT EXISTS subcategory TEXT,
ADD COLUMN IF NOT EXISTS is_reimbursable BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS is_tax_deductible BOOLEAN DEFAULT false;

-- Create index for category filtering
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);
CREATE INDEX IF NOT EXISTS idx_expenses_reimbursable ON expenses(is_reimbursable) WHERE is_reimbursable = true;

-- Add check constraint for valid categories
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'expenses_category_check'
  ) THEN
    ALTER TABLE expenses ADD CONSTRAINT expenses_category_check 
    CHECK (category IN ('business', 'personal', 'customer_purchase', 'other', 'uncategorized'));
  END IF;
END $$;

-- Add comment for documentation
COMMENT ON COLUMN expenses.category IS 'Expense category: business (tax deductible), personal (owner withdrawal), customer_purchase (reimbursable), other';
COMMENT ON COLUMN expenses.is_reimbursable IS 'True if expense should be reimbursed by customer or company';
COMMENT ON COLUMN expenses.is_tax_deductible IS 'True if expense qualifies as tax deduction';
