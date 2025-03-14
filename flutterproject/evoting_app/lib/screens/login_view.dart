import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  LoginViewState createState() => LoginViewState();
}

class LoginViewState extends State<LoginView> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _login() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await http.post(
        Uri.parse('http://192.168.0.170:8000/apilogin/'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "username": _usernameController.text,
          "password": _passwordController.text,
        }),
      );
      print(response.body);
      if (!mounted) return; 

      setState(() {
        _isLoading = false;
      });

      if (response.statusCode == 200) {
        Navigator.pushReplacementNamed(context, "/dashboard"); 
      } else {
        setState(() {
          _errorMessage = "Invalid username or password. Please try again.";
        });
      }
    } catch (e) {
      if (!mounted) return; 
      print("An error occured: ${e.toString()}");
      setState(() {
        _isLoading = false;
        _errorMessage = "Network error. Please try again.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("eVoting Login")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Login", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
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

            // Login Button
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _login,
                    child: const Text("Log In"),
                  ),

            const SizedBox(height: 10),

            // Forgot Password Link
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, "/forgot-password");
              },
              child: const Text("Forgot Password?", style: TextStyle(color: Colors.red)),
            ),

            // Register Link
            const Text("Don't have an account?"),
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, "/register");
              },
              child: const Text("Register"),
            ),
          ],
        ),
      ),
    );
  }
}
