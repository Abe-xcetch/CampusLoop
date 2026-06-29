/**
 * Strathmore University Email Verification Rules
 */
export declare const ALLOWED_EMAIL_DOMAINS: readonly ["strathmore.edu", "su.strathmore.edu", "alumni.strathmore.edu"];
export declare const STRATHMORE_EMAIL_REGEX: RegExp;
/**
 * Marketplace Listing Constants
 */
export declare const LISTING_STATUS: {
    readonly DRAFT: "DRAFT";
    readonly PENDING_APPROVAL: "PENDING_APPROVAL";
    readonly ACTIVE: "ACTIVE";
    readonly SOLD: "SOLD";
    readonly FLAGGED: "FLAGGED";
    readonly ARCHIVED: "ARCHIVED";
};
export type ListingStatus = typeof LISTING_STATUS[keyof typeof LISTING_STATUS];
export declare const CATEGORIES: readonly [{
    readonly name: "Textbooks & Stationery";
    readonly slug: "textbooks-stationery";
}, {
    readonly name: "Electronics & Gadgets";
    readonly slug: "electronics-gadgets";
}, {
    readonly name: "Clothing & Fashion";
    readonly slug: "clothing-fashion";
}, {
    readonly name: "Hostel Essentials & Furniture";
    readonly slug: "hostel-essentials-furniture";
}, {
    readonly name: "Services & Tutoring";
    readonly slug: "services-tutoring";
}, {
    readonly name: "Other";
    readonly slug: "other";
}];
/**
 * Transaction Lifecycle Constants
 */
export declare const TRANSACTION_STATUS: {
    readonly INITIATED: "INITIATED";
    readonly CONFIRMED: "CONFIRMED";
    readonly COMPLETED: "COMPLETED";
    readonly CANCELLED: "CANCELLED";
};
export type TransactionStatus = typeof TRANSACTION_STATUS[keyof typeof TRANSACTION_STATUS];
/**
 * Fraud Moderation Constants
 */
export declare const REPORT_STATUS: {
    readonly OPEN: "OPEN";
    readonly INVESTIGATING: "INVESTIGATING";
    readonly RESOLVED_NO_ACTION: "RESOLVED_NO_ACTION";
    readonly RESOLVED_LISTING_REMOVED: "RESOLVED_LISTING_REMOVED";
    readonly RESOLVED_USER_BANNED: "RESOLVED_USER_BANNED";
};
export type ReportStatus = typeof REPORT_STATUS[keyof typeof REPORT_STATUS];
export declare const REPORT_REASONS: {
    readonly FRAUD_SCAM: "FRAUD_SCAM";
    readonly INAPPROPRIATE_CONTENT: "INAPPROPRIATE_CONTENT";
    readonly COUNTERFEIT: "COUNTERFEIT";
    readonly OUT_OF_STOCK_SPAM: "OUT_OF_STOCK_SPAM";
    readonly OTHER: "OTHER";
};
/**
 * User Roles
 */
export declare const USER_ROLES: {
    readonly STUDENT: "STUDENT";
    readonly ADMIN: "ADMIN";
    readonly SUPERADMIN: "SUPERADMIN";
};
export type UserRole = typeof USER_ROLES[keyof typeof USER_ROLES];
//# sourceMappingURL=index.d.ts.map