import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ForgotPasswordView extends StatefulWidget {
  const ForgotPasswordView({super.key});  

  @override
  ForgotPasswordViewState createState() => ForgotPasswordViewState(); 
}

class ForgotPasswordViewState extends State<ForgotPasswordView> { 
  final TextEditingController _emailController = TextEditingController();
  bool _isLoading = false;
  String? _message;

  Future<void> _resetPassword() async {
    setState(() {
      _isLoading = true;
      _message = null;
    });

    try {
      final response = await http.post(
        Uri.parse('https://your-backend.com/api/forgot-password'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"email": _emailController.text}),
      );

      setState(() {
        _isLoading = false;
        _message = response.statusCode == 200
            ? "Check your email for reset link."
            : "Error sending reset link.";
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _message = "Network error. Please try again.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Forgot Password")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: "Email"),
              keyboardType: TextInputType.emailAddress,
            ),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Text(
                  _message!,
                  style: TextStyle(
                    color: _message == "Check your email for reset link."
                        ? Colors.green
                        : Colors.red,
                  ),
                ),
              ),
            const SizedBox(height: 20),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _resetPassword,
                    child: const Text("Reset Password"),
                  ),
          ],
        ),
      ),
    );
  }
}
