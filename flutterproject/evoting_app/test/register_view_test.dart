import 'package:evoting_app/screens/register_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Register screen UI test', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: RegisterView()));

    // Verify TextFields exist
    expect(find.byType(TextField), findsNWidgets(4)); // Name, Email, Password, Phone Number
    expect(find.widgetWithText(TextField, "Name"), findsOneWidget);  // Name label
    expect(find.widgetWithText(TextField, "Email"), findsOneWidget); // Email label
    expect(find.widgetWithText(TextField, "Password"), findsOneWidget); // Password label
    expect(find.widgetWithText(TextField, "PhoneNumber"), findsOneWidget); // Phone Number label
    
    // Verify Register button exists
    expect(find.text("Register"), findsOneWidget);

    // Enter text into Name, Email, Password, and Phone Number fields
    await tester.enterText(find.byType(TextField).at(0), "testuser");
    await tester.enterText(find.byType(TextField).at(1), "testuser@example.com");
    await tester.enterText(find.byType(TextField).at(2), "password123");
    await tester.enterText(find.byType(TextField).at(3), "1234567890");

    // Tap Register button
    await tester.tap(find.text("Register"));
    await tester.pumpAndSettle(); // Wait for animations and async operations to complete

    // Verify loading state (if applicable)
    expect(find.byType(CircularProgressIndicator), findsNothing); // Adjust based on the actual behavior of the app
  });
}
