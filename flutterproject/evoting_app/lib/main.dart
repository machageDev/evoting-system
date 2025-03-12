

import 'package:flutter/material.dart';
import 'screens/login_view.dart';
import 'screens/register_view.dart';
import 'screens/forgot_password_view.dart';
import 'screens/dashboard_view.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'eVoting System',
      theme: ThemeData(primarySwatch: Colors.blue),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginView(),
        '/register': (context) => const RegisterView(),
        '/forgot-password': (context) => const ForgotPasswordView(),
        '/dashboard': (context) => DashboardView(),
      },
    );
  }
}
