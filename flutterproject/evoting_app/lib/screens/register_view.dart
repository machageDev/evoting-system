import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class RegisterView extends StatefulWidget {
  const RegisterView({super.key}); // ✅ Added super.key

  @override
  RegisterViewState createState() => RegisterViewState(); // ✅ Removed `_`
}

class RegisterViewState extends State<RegisterView> { // ✅ Removed `_`
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _register() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await http.post(
        Uri.parse('https://your-backend.com/api/register/'), // 🔹 Replace with your Django API URL
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "username": _usernameController.text, // 🔹 Match Django username field
          "password": _passwordController.text,
        }),
      );

      setState(() {
        _isLoading = false;
      });

      if (response.statusCode == 201) {
        // ✅ Successful registration, navigate to login
        Navigator.pushReplacementNamed(context, "/login");
      } else {
        // ❌ Registration failed, show an error
        setState(() {
          _errorMessage = "Registration failed. Please try again.";
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = "Network error. Please check your connection.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Register")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Create an Account", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),

            // Username Field
            TextField(
              controller: _usernameController,
              decoration: const InputDecoration(labelText: "Username"),
              keyboardType: TextInputType.text,
            ),
            const SizedBox(height: 10),

            // Password Field
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: "Password"),
              keyboardType: TextInputType.visiblePassword,
            ),
            const SizedBox(height: 10),

            // Error Message
            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.red),
                ),
              ),

            // Register Button
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _register,
                    child: const Text("Register"),
                  ),

            const SizedBox(height: 10),

            // Already have an account?
            const Text("Already have an account?"),
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, "/login");
              },
              child: const Text("Log In"),
            ),
          ],
        ),
      ),
    );
  }
}
