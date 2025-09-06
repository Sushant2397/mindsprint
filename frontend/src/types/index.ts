// User types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  locale: string;
  kyc_status: 'pending' | 'verified' | 'rejected';
  avatar?: string;
  date_joined: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone?: string;
}

// Group types
export interface Group {
  id: number;
  name: string;
  description: string;
  group_type: 'roommates' | 'society' | 'club' | 'family' | 'friends' | 'business' | 'other';
  owner: User;
  settings: Record<string, any>;
  currency: string;
  billing_cycle: string;
  gst_mode: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  members: GroupMember[];
  member_count: number;
}

export interface GroupMember {
  id: number;
  user: User;
  role: 'owner' | 'treasurer' | 'auditor' | 'member';
  share_factor: number;
  income_bracket: 'low' | 'medium' | 'high';
  joined_at: string;
  is_active: boolean;
}

// Expense types
export interface Expense {
  id: number;
  group: number;
  payer: User;
  amount_subtotal: number;
  amount_tax: number;
  total_amount: number;
  vendor: string;
  gstin?: string;
  invoice_no?: string;
  category: string;
  description: string;
  date: string;
  receipt_file?: string;
  ocr_data: Record<string, any>;
  is_settled: boolean;
  created_at: string;
  updated_at: string;
  splits: ExpenseSplit[];
}

export interface ExpenseSplit {
  id: number;
  member: User;
  amount_owed: number;
  split_type: 'equal' | 'percentage' | 'amount' | 'share_factor';
  metadata: Record<string, any>;
  is_paid: boolean;
  created_at: string;
}

// Payment types
export interface LedgerEntry {
  id: number;
  from_member: User;
  to_member: User;
  amount: number;
  status: 'pending' | 'paid' | 'cancelled' | 'disputed';
  ref_expense?: Expense;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: number;
  ledger_entry: LedgerEntry;
  method: 'UPI_DEEPLINK' | 'UPI_AUTOPAY' | 'MANUAL' | 'CASH' | 'BANK_TRANSFER';
  payment_ref: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  amount: number;
  upi_deeplink?: string;
  webhook_data: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Settlement types
export interface SettlementTransaction {
  from_member: number;
  to_member: number;
  amount: number;
  explanation: string;
}

export interface SettlementGraph {
  nodes: Array<{
    id: number;
    username: string;
    role: string;
  }>;
  edges: Array<{
    from: number;
    to: number;
    amount: number;
    explanation: string;
  }>;
}

export interface SettlementResult {
  group_id: number;
  group_name: string;
  policy_type: string;
  total_settlement_amount: number;
  transaction_count: number;
  transactions: SettlementTransaction[];
  graph: SettlementGraph;
  member_balances: Record<string, number>;
}

// Consent types
export interface Consent {
  id: number;
  user: number;
  purpose: 'expense_analysis' | 'settlement_calculation' | 'group_insights' | 'payment_processing';
  audience: 'group_members' | 'group_owner' | 'system' | 'third_party';
  scope: Record<string, any>;
  consent_token: string;
  is_active: boolean;
  expires_at: string;
  created_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// UI State types
export interface Theme {
  mode: 'light' | 'dark';
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: number;
  read: boolean;
}

export interface SyncStatus {
  isOnline: boolean;
  lastSync: number;
  pendingChanges: number;
}

// Form types
export interface AddExpenseForm {
  group_id: number;
  amount_subtotal: number;
  amount_tax: number;
  vendor: string;
  gstin?: string;
  invoice_no?: string;
  category: string;
  description: string;
  date: string;
  receipt_file?: File;
}

export interface CreateGroupForm {
  name: string;
  description: string;
  group_type: string;
  currency: string;
  billing_cycle: string;
  gst_mode: boolean;
}

// Export types
export interface ExportOptions {
  format: 'csv' | 'pdf';
  date_from?: string;
  date_to?: string;
  include_receipts?: boolean;
}

// Fairness Policy types
export interface FairnessPolicy {
  id: number;
  group: number;
  policy_type: 'equal_split' | 'income_based' | 'custom_share' | 'proportional';
  parameters: Record<string, any>;
  is_active: boolean;
  created_at: string;
  created_by: User;
}