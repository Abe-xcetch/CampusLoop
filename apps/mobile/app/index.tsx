import React from "react";
import { View, Text, TouchableOpacity, ScrollView } from "react-native";
import { Link, useRouter } from "expo-router";

export default function HomeIndexScreen() {
  const router = useRouter();

  return (
    <ScrollView className="flex-1 bg-slate-50">
      <View className="px-6 py-12 items-center">
        {/* Logo Icon */}
        <View className="h-16 w-16 bg-strathmore-blue rounded-2xl items-center justify-center shadow-lg shadow-strathmore-blue/20 mb-8">
          <Text className="text-white font-extrabold text-2xl">CL</Text>
        </View>

        <Text className="text-xs uppercase font-bold tracking-wider text-strathmore-blue bg-blue-100/50 px-3 py-1 rounded-full mb-4">
          Strathmore University
        </Text>

        <Text className="text-3xl font-extrabold text-center text-slate-900 leading-tight">
          Verified Student Marketplace
        </Text>

        <Text className="text-base text-slate-600 text-center mt-4 mb-10 leading-relaxed px-2">
          Buy and sell items within campus securely. All accounts are validated using student emails.
        </Text>

        {/* Action Buttons */}
        <TouchableOpacity
          className="w-full bg-strathmore-blue py-4 rounded-xl items-center shadow-md mb-4"
          onPress={() => router.push("/listings")}
        >
          <Text className="text-white font-bold text-base">Browse Listings</Text>
        </TouchableOpacity>

        <TouchableOpacity
          className="w-full bg-white border border-slate-200 py-4 rounded-xl items-center shadow-sm"
          onPress={() => router.push("/auth/login")}
        >
          <Text className="text-slate-800 font-semibold text-base">Get Started</Text>
        </TouchableOpacity>
      </View>

      {/* Trust Badges */}
      <View className="px-6 border-t border-slate-200 py-8 bg-slate-100/50">
        <Text className="font-bold text-lg text-slate-800 mb-4">Why use CampusLoop?</Text>
        
        <View className="mb-4">
          <Text className="font-bold text-slate-900 text-sm">🔒 Verified Users</Text>
          <Text className="text-xs text-slate-600 mt-1">
            Signups are restricted to @strathmore.edu emails to ensure safety.
          </Text>
        </View>

        <View className="mb-4">
          <Text className="font-bold text-slate-900 text-sm">⭐ Reputation Tracking</Text>
          <Text className="text-xs text-slate-600 mt-1">
            Ratings are only allowed after a verified successful transaction.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}
