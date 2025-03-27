import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.0.102:8000';
  static const String loginUrl = '$baseUrl/apilogin';
  static const String forgot_passwordUrl = '$baseUrl/apiforgot_password';
  static const String registerUrl = '$baseUrl/apiregister';
  static const String electionUrl = '$baseUrl/apielections';
  static const String candidateUrl = '$baseUrl/apicandidates';
  static const String voteUrl = '$baseUrl/apivote';
  static const String resultUrl = '$baseUrl/api_result';
  static const String dashboardUrl ='$baseUrl/api/dashboard';
  static const String homepageUrl = '$baseUrl/api_home';
  static const String homeUrl = 'http://192.168.0.102:8000/api_home'; 
  static const String candidateDetailUrl = '$baseUrl/api_get_candidate';  


  // ✅ FETCH DATA FUNCTION
  Future<String> fetchData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/apiregister'));

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
  static Future<Map<String, dynamic>> loginUser(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse(loginUrl),
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: {'username': username, 'password': password},
      );

      return jsonDecode(response.body);
    } catch (e) {
      return {"success": false, "message": "Login failed: $e"};
    }
  }

  // ✅ REGISTER FUNCTION
  static Future<Map<String, dynamic>> register(
      String name, String email, String password, String phoneNumber) async {
    final url = Uri.parse(registerUrl);

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "name": name,
          "email": email,
          "password": password,
          "phone_number": phoneNumber,
        }),
      );

      if (response.statusCode == 201) {
        return {"success": true};
      } else {
        return {"success": false, "message": jsonDecode(response.body)["error"]};
      }
    } catch (e) {
      return {"success": false, "message": "Network error, please try again."};
    }
  }

  // ✅ CREATE ELECTION FUNCTION
  Future<bool> createElection(String name, String date, String status) async {
    final url = Uri.parse(electionUrl);

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'name': name, 'date': date, 'status': status}),
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

   // Fetch voter details
  static Future<Map<String, dynamic>> getUserDetails(int UserId) async {
    Uri url = Uri.parse('$baseUrl/voter/$UserId/');
    final response = await http.get(url);
    return _processResponse(response);
  }

  // Fetch active elections
  static Future<List<dynamic>> getActiveElections() async {
    Uri url = Uri.parse('$baseUrl/elections/active/');
    final response = await http.get(url);
    return _processResponse(response);
  }

  // Cast a vote
  static Future<Map<String, dynamic>> castVote(int voterId, int electionId, int candidateId) async {
    Uri url = Uri.parse('$baseUrl/vote');
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "voter_id": voterId,
        "election_id": electionId,
        "candidate_id": candidateId
      }),
    );
    return _processResponse(response);
  }

  // Fetch election results
  static Future<Map<String, dynamic>> getElectionResults(int electionId) async {
    Uri url = Uri.parse('$baseUrl/election/${electionId.toString()}/results/');
    final response = await http.get(url);
    return _processResponse(response);
  }

  // Common response handler
  static dynamic _processResponse(http.Response response) {
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {"success": false, "error": "Failed to fetch data"};
    }
  }

  static getVoterDashboard() {}

  static forgot_Password(String email) {}

  static fetchCandidates() {}
}

   Future<Map<String, dynamic>> getElectionResults(int electionId, dynamic baseUrl) async {
    final response = await http.get(Uri.parse("$baseUrl/api_result/"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load election results");
    }
  }
Future<String> fetchWelcomeMessage(dynamic home, dynamic baseUrl) async {
    try {
      final String apiUrl = '$baseUrl$home';  

      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['message'] ?? "Welcome to the eVoting System";  
      } else {
        throw Exception("Failed to load data");
      }
    } catch (e) {
      throw Exception("Error fetching data: $e");
    }
  }

Future<Map<String, dynamic>> forgotPassword(String email, dynamic baseUrl) async {
    final url = Uri.parse('$baseUrl/forgot_password');

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'email': email}),
      );

      if (response.statusCode == 200) {
        return {
          'status': true,
          'message': 'Check your email for reset link.',
        };
      } else {
        // If your API returns an error message in the body
        final data = json.decode(response.body);
        return {
          'status': false,
          'message': data['error'] ?? 'Failed to send reset email.',
        };
      }
    } catch (e) {
      return {
        'status': false,
        'message': 'Something went wrong. Please try again later.',
      };
    }

}  
  // Fetch dashboard data (Active & Pending Elections)
 Future<Map<String, dynamic>> fetchDashboardData(dynamic baseUrl) async {
    final url = Uri.parse("$baseUrl/api/dashboard");

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {
          'status': false,
          'message': 'Failed to load dashboard data',
          'error': response.body
        };
      }
    } catch (e) {
      return {
        'status': false,
        'message': 'An error occurred',
        'error': e.toString()
      };
    }
  }
   //Function to fetch home page data
  Future<Map<String, dynamic>> fetchHomePageData(dynamic baseUrl) async {
    const String homeUrl = 'api_home'; // Your home page data endpoint
    try {
      final response = await http.get(Uri.parse(baseUrl + homeUrl));

      if (response.statusCode == 200) {
        // Assuming the response is in JSON format
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load home page data');
      }
    } catch (e) {
      throw Exception('Error fetching data: $e');
    }
  }

  Future<List<Map<String, dynamic>>> getCandidates(dynamic baseUrl) async {
    final response = await http.get(Uri.parse('$baseUrl/candidates/'));
    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(json.decode(response.body));
    } else {
      throw Exception('Failed to load candidates');
    }
  }

  // Update candidate
   Future<void> updateCandidate(int id, String name, String position, dynamic baseUrl) async {
    final response = await http.put(
      Uri.parse('$baseUrl/candidates/$id/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'position': position}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update candidate');
    }
  }

  // Delete candidate
   Future<void> deleteCandidate(int id, dynamic baseUrl) async {
    final response = await http.delete(Uri.parse('$baseUrl/candidates/$id/'));
    if (response.statusCode != 204) {
      throw Exception('Failed to delete candidate');
    }
  }