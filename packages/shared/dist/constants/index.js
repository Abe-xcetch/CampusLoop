"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.USER_ROLES = exports.REPORT_REASONS = exports.REPORT_STATUS = exports.TRANSACTION_STATUS = exports.CATEGORIES = exports.LISTING_STATUS = exports.STRATHMORE_EMAIL_REGEX = exports.ALLOWED_EMAIL_DOMAINS = void 0;
/**
 * Strathmore University Email Verification Rules
 */
exports.ALLOWED_EMAIL_DOMAINS = [
    "strathmore.edu",
    "su.strathmore.edu",
    "alumni.strathmore.edu"
];
exports.STRATHMORE_EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@(su\.)?strathmore\.edu$/;
/**
 * Marketplace Listing Constants
 */
exports.LISTING_STATUS = {
    DRAFT: "DRAFT",
    PENDING_APPROVAL: "PENDING_APPROVAL",
    ACTIVE: "ACTIVE",
    SOLD: "SOLD",
    FLAGGED: "FLAGGED",
    ARCHIVED: "ARCHIVED"
};
exports.CATEGORIES = [
    { name: "Textbooks & Stationery", slug: "textbooks-stationery" },
    { name: "Electronics & Gadgets", slug: "electronics-gadgets" },
    { name: "Clothing & Fashion", slug: "clothing-fashion" },
    { name: "Hostel Essentials & Furniture", slug: "hostel-essentials-furniture" },
    { name: "Services & Tutoring", slug: "services-tutoring" },
    { name: "Other", slug: "other" }
];
/**
 * Transaction Lifecycle Constants
 */
exports.TRANSACTION_STATUS = {
    INITIATED: "INITIATED",
    CONFIRMED: "CONFIRMED", // Seller confirmed availability
    COMPLETED: "COMPLETED", // Buyer confirmed hand-off
    CANCELLED: "CANCELLED"
};
/**
 * Fraud Moderation Constants
 */
exports.REPORT_STATUS = {
    OPEN: "OPEN",
    INVESTIGATING: "INVESTIGATING",
    RESOLVED_NO_ACTION: "RESOLVED_NO_ACTION",
    RESOLVED_LISTING_REMOVED: "RESOLVED_LISTING_REMOVED",
    RESOLVED_USER_BANNED: "RESOLVED_USER_BANNED"
};
exports.REPORT_REASONS = {
    FRAUD_SCAM: "FRAUD_SCAM",
    INAPPROPRIATE_CONTENT: "INAPPROPRIATE_CONTENT",
    COUNTERFEIT: "COUNTERFEIT",
    OUT_OF_STOCK_SPAM: "OUT_OF_STOCK_SPAM",
    OTHER: "OTHER"
};
/**
 * User Roles
 */
exports.USER_ROLES = {
    STUDENT: "STUDENT",
    ADMIN: "ADMIN",
    SUPERADMIN: "SUPERADMIN"
};
//# sourceMappingURL=index.js.map