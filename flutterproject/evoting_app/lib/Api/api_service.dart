import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.137.1:8000';
  static const String loginUrl = '$baseUrl/apilogin';
  static const String registerUrl = '$baseUrl/apiregister';

  // ✅ LOGIN FUNCTION
  static Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.137.1:8000/apilogin'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
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
  static Future<Map<String, dynamic>> register(String name, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.168.137.1:8000/apiregister'), // ✅ Corrected URL
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': name,
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'message': 'Registration failed. Please try again.'};
      }
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }
}

  // API function to create election
  Future<bool> createElection(String name, String date, String status) async {
    final url = Uri.parse('http://192.168.137.1:8000/apielections'); // Add your endpoint here

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'name': name,
          'date': date,
          'status': status,
        }),
      );

      if (response.statusCode == 201) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
      print('Error: $e');
      return false;
    }
  }

   Future<bool> uploadCandidate(
      String name, String position, File? image) async {
    var request = http.MultipartRequest(
        "POST", Uri.parse("http://127.168.0.122:8000/apicreate_candidate"));

    // Attach Form Data
    request.fields["name"] = name;
    request.fields["position"] = position;
    request.fields["election"] = "1"; // assuming election ID is 1

    // Attach Image if exists
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

      if (response.statusCode == 201) {
        return true;
      } else {
        print("❌ Error: ${response.reasonPhrase}");
        return false;
      }
    } catch (e) {
      print("❌ Error: $e");
      return false;
    }
      }


