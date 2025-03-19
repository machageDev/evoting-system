import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.0.54:8000';
  static const String loginUrl = '$baseUrl/api/login';
  static const String registerUrl = 'http://192.168.0.54:8000/apiregister';


  Future<String> fetchData() async {
  try {
    final response = await http.get(Uri.parse('http://192.168.0.54:8000/api/register'));

    if (response.statusCode == 200) {
      return response.body; 
    } else {
      return "Error: Failed to load data"; 
    }
  } catch (e) {
    return "Error: $e";
  }
}


  // ✅ LOGIN FUNCTION
  static Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/apilogin'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'message': 'Invalid username or password.'};
      }
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // ✅ REGISTER FUNCTION
  static Future<Map<String, dynamic>> register(
      String name, String email, String password, String phoneNumber) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/apiregister'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': name,
          'email': email,
          'password': password,
          'phone_number': phoneNumber,
        }),
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data};
      } else {
        final errorMessage = jsonDecode(response.body)['message'] ?? 'Registration failed. Please try again.';
        return {'success': false, 'message': errorMessage};
      }
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // ✅ CREATE ELECTION FUNCTION
  Future<bool> createElection(String name, String date, String status) async {
    final url = Uri.parse('$baseUrl/apielections');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'name': name, 'date': date, 'status': status}),
      );

      return response.statusCode == 201;
    } catch (e) {
      debugPrint('Error: $e');
      return false;
    }
  }

  // ✅ UPLOAD CANDIDATE FUNCTION
  Future<bool> uploadCandidate(String name, String position, File? image) async {
    var request = http.MultipartRequest("POST", Uri.parse("$baseUrl/apicreate_candidate"));

    request.fields["name"] = name;
    request.fields["position"] = position;
    request.fields["election"] = "1"; // Assuming election ID is 1

    if (image != null) {
      request.files.add(
        await http.MultipartFile.fromPath(
          "profile_picture",
          image.path,
          contentType: MediaType("image", "jpeg"),
        ),
      );
    }

    try {
      var response = await request.send();
      return response.statusCode == 201;
    } catch (e) {
      debugPrint("❌ Error: $e");
      return false;
    }
  }

  // ✅ FETCH ELECTION RESULTS FUNCTION
  Future<List<dynamic>> fetchElectionResults(int electionId) async {
    final url = Uri.parse('$baseUrl/api/election_results/$electionId');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception("Failed to load results.");
      }
    } catch (e) {
      throw Exception("Error: $e");
    }
  }
}
