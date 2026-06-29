/**
 * Strathmore University Email Verification Rules
 */
export const ALLOWED_EMAIL_DOMAINS = [
  "strathmore.edu",
  "su.strathmore.edu",
  "alumni.strathmore.edu"
] as const;

export const STRATHMORE_EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@(su\.)?strathmore\.edu$/;

/**
 * Marketplace Listing Constants
 */
export const LISTING_STATUS = {
  DRAFT: "DRAFT",
  PENDING_APPROVAL: "PENDING_APPROVAL",
  ACTIVE: "ACTIVE",
  SOLD: "SOLD",
  FLAGGED: "FLAGGED",
  ARCHIVED: "ARCHIVED"
} as const;

export type ListingStatus = typeof LISTING_STATUS[keyof typeof LISTING_STATUS];

export const CATEGORIES = [
  { name: "Textbooks & Stationery", slug: "textbooks-stationery" },
  { name: "Electronics & Gadgets", slug: "electronics-gadgets" },
  { name: "Clothing & Fashion", slug: "clothing-fashion" },
  { name: "Hostel Essentials & Furniture", slug: "hostel-essentials-furniture" },
  { name: "Services & Tutoring", slug: "services-tutoring" },
  { name: "Other", slug: "other" }
] as const;

/**
 * Transaction Lifecycle Constants
 */
export const TRANSACTION_STATUS = {
  INITIATED: "INITIATED",
  CONFIRMED: "CONFIRMED", // Seller confirmed availability
  COMPLETED: "COMPLETED", // Buyer confirmed hand-off
  CANCELLED: "CANCELLED"
} as const;

export type TransactionStatus = typeof TRANSACTION_STATUS[keyof typeof TRANSACTION_STATUS];

/**
 * Fraud Moderation Constants
 */
export const REPORT_STATUS = {
  OPEN: "OPEN",
  INVESTIGATING: "INVESTIGATING",
  RESOLVED_NO_ACTION: "RESOLVED_NO_ACTION",
  RESOLVED_LISTING_REMOVED: "RESOLVED_LISTING_REMOVED",
  RESOLVED_USER_BANNED: "RESOLVED_USER_BANNED"
} as const;

export type ReportStatus = typeof REPORT_STATUS[keyof typeof REPORT_STATUS];

export const REPORT_REASONS = {
  FRAUD_SCAM: "FRAUD_SCAM",
  INAPPROPRIATE_CONTENT: "INAPPROPRIATE_CONTENT",
  COUNTERFEIT: "COUNTERFEIT",
  OUT_OF_STOCK_SPAM: "OUT_OF_STOCK_SPAM",
  OTHER: "OTHER"
} as const;

/**
 * User Roles
 */
export const USER_ROLES = {
  STUDENT: "STUDENT",
  ADMIN: "ADMIN",
  SUPERADMIN: "SUPERADMIN"
} as const;

export type UserRole = typeof USER_ROLES[keyof typeof USER_ROLES];
