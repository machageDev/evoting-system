import 'package:evoting_app/screens/login_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Login screen UI test', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginView()));

    // Verify TextFields exist
    expect(find.byType(TextField), findsNWidgets(2)); // Username & Password
    expect(find.text("Username"), findsOneWidget);
    expect(find.text("Password"), findsOneWidget);

    // Verify Login button exists
    expect(find.text("Log In"), findsOneWidget);

    // Verify navigation links exist
    expect(find.text("Forgot Password?"), findsOneWidget);
    expect(find.text("Register"), findsOneWidget);

    // Enter text into username and password fields
    await tester.enterText(find.byType(TextField).at(0), "testuser");
    await tester.enterText(find.byType(TextField).at(1), "password123");

    // Tap Login button
    await tester.tap(find.text("Log In"));
    await tester.pump(); // Rebuild UI

    // Verify loading state (if applicable)
    expect(find.byType(CircularProgressIndicator), findsNothing);
  });
}
