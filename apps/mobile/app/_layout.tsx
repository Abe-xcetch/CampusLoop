import { Stack } from "expo-router";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: "#003366", // Strathmore Blue
          },
          headerTintColor: "#ffffff",
          headerTitleStyle: {
            fontWeight: "bold",
          },
        }}
      >
        <Stack.Screen
          name="index"
          options={{
            title: "CampusLoop",
          }}
        />
        <Stack.Screen
          name="listings/index"
          options={{
            title: "Marketplace",
          }}
        />
        <Stack.Screen
          name="auth/login"
          options={{
            title: "Sign In",
            presentation: "modal",
          }}
        />
      </Stack>
    </SafeAreaProvider>
  );
}
