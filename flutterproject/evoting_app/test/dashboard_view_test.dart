import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:evoting_app/home/dashboard_view.dart';  

void main() {
  testWidgets('Dashboard UI and Navigation Test', (WidgetTester tester) async {
    // Build the DashboardView
    await tester.pumpWidget(MaterialApp(home: Dashboard()));

    // Check if key UI elements exist
    expect(find.text('Dashboard'), findsOneWidget);
    expect(find.text('Candidates'), findsOneWidget);
    expect(find.text('Results'), findsOneWidget);
    expect(find.text('Profile'), findsOneWidget);
    expect(find.text('Settings'), findsOneWidget);

    // Simulate tapping on "Candidates"
    await tester.tap(find.text('Candidates'));
    await tester.pumpAndSettle();

    // Verify if the Candidates screen is displayed
    expect(find.text('Candidates Screen'), findsOneWidget);
  });
}
