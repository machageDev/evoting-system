import 'package:evoting_app/screens/forgot_password_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Forgot Password screen UI test', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: ForgotPasswordView()));

    // Verify TextField exists
    expect(find.byType(TextField), findsOneWidget);
    expect(find.text("Email"), findsOneWidget);

    // Verify Reset Password button exists
    expect(find.text("Reset Password"), findsOneWidget);

    // Enter email
    await tester.enterText(find.byType(TextField), "test@example.com");

    // Tap Reset Password button
    await tester.tap(find.text("Reset Password"));
    await tester.pump(); // Rebuild UI

    // Verify loading state (if applicable)
    expect(find.byType(CircularProgressIndicator), findsNothing);
  });
}

