import { ListingStatus, TransactionStatus, ReportStatus, UserRole } from "../constants/index.js";

export interface User {
  id: string; // Firebase UID
  email: string; // Must end with @strathmore.edu or @su.strathmore.edu
  firstName: string;
  lastName: string;
  avatarUrl?: string;
  phoneNumber?: string;
  role: UserRole;
  isVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Verification {
  id: string;
  userId: string;
  isEmailVerified: boolean;
  verifiedAt?: string;
  verificationToken?: string;
  expiresAt?: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  parentId?: string;
}

export interface Listing {
  id: string;
  title: string;
  description: string;
  price: number;
  condition: "NEW" | "LIKE_NEW" | "GOOD" | "FAIR";
  mediaUrls: string[];
  status: ListingStatus;
  categoryId: string;
  categoryName: string;
  sellerId: string;
  sellerName: string;
  sellerAvatar?: string;
  createdAt: string;
  updatedAt: string;
  approvedAt?: string;
  approvedById?: string;
}

export interface Transaction {
  id: string;
  listingId: string;
  listingTitle: string;
  listingPrice: number;
  buyerId: string;
  buyerName: string;
  sellerId: string;
  sellerName: string;
  status: TransactionStatus;
  initiatedAt: string;
  confirmedAt?: string;
  completedAt?: string;
  cancelledAt?: string;
  cancellationReason?: string;
}

export interface Review {
  id: string;
  transactionId: string;
  reviewerId: string;
  reviewerName: string;
  revieweeId: string;
  rating: number; // 1 to 5
  comment: string;
  createdAt: string;
}

export interface ReputationScore {
  userId: string;
  ratingAverage: number;
  totalRatingsCount: number;
  completedTransactionsCount: number;
  isTrustedSeller: boolean;
}

export interface FraudReport {
  id: string;
  reporterId: string;
  reportedUserId?: string;
  reportedListingId?: string;
  reason: string;
  details: string;
  status: ReportStatus;
  createdAt: string;
  resolvedAt?: string;
  resolvedById?: string;
  resolutionNotes?: string;
}

export interface AdminAction {
  id: string;
  adminId: string;
  actionType: "APPROVE_LISTING" | "REJECT_LISTING" | "BAN_USER" | "UNBAN_USER" | "RESOLVE_REPORT";
  targetId: string;
  notes: string;
  createdAt: string;
}

export interface Notification {
  id: string;
  userId: string;
  title: string;
  body: string;
  type: "TRANSACTION_UPDATE" | "NEW_REVIEW" | "LISTING_APPROVED" | "REPORT_ALERT" | "GENERAL";
  isRead: boolean;
  redirectPath?: string;
  createdAt: string;
}
