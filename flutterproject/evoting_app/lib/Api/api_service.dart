import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.0.27:8000';  
  static const String candidateUrl = '$baseUrl/apiget_candidates';
  static const String dashboardUrl ='$baseUrl/api/dashboard';
  static const String electionUrl = '$baseUrl/api/elections/results';
  static const String forgot_passwordUrl = '$baseUrl/apiforgot_password';
  static const String homeUrl = 'http://192.168.0.27:8000/api_home'; 
  static const String homepageUrl = '$baseUrl/api_home';
  static const String loginUrl = '$baseUrl/apilogin';
  static const String managecandidateUrl ='$baseUrl/apimanage_candidate';
  static const String manageelctionUrl ='$baseUrl/apimanage_election';
  static const String registerUrl = '$baseUrl/apiregister';
  static const String resultUrl = '$baseUrl/api_result';
  static const String voteUrl = '$baseUrl/apivote';
  static const  String CreateElctionUrl='$baseUrl/apicreate_election';
  static const String  ProfileViewUrl = '$baseUrl/apicreate_profile';
  static const String  getVoterDashboardUrl = 'baseUrl/api_voter_dashboard';
  static const String getelectionUrl = '$baseUrl/apielection';

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

  static getVoterDashboard() {}

  static forgot_Password(String email) {}

  static fetchCandidates() {}

  // Common response handler
  static dynamic _processResponse(http.Response response) {
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {"success": false, "error": "Failed to fetch data"};
    }
  }
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

Future<List<Map<String, dynamic>>> getCandidates(String baseUrl) async {
    final response = await http.get(Uri.parse('$baseUrl/candidates/<str:election>'));
    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(json.decode(response.body));
    } else {
      throw Exception('Failed to load candidates');
    }
  }

  Future<void> updateCandidate(int id, String name, String position, String baseUrl) async {
    final response = await http.put(
      Uri.parse('$baseUrl/candidates/$id/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'position': position}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update candidate');
    }
  }

  Future<void> deleteCandidate(int id, String baseUrl) async {
    final response = await http.delete(Uri.parse('$baseUrl/candidates/$id/'));
    if (response.statusCode != 204) {
      throw Exception('Failed to delete candidate');
    }
  }

  Future<Map<String, dynamic>?> getUserProfile(String token, dynamic baseUrl) async {
    final response = await http.get(
      Uri.parse('$baseUrl/apicreate_profile'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return null;
    }
  }
   Future<Map<String, dynamic>?> getVoterDashboard(dynamic baseUrl) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api_voter_dashboard'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Error: ${response.statusCode} - ${response.body}");
        return null;
      }
    } catch (error) {
      print("Exception: $error");
      return null;
    }
  }

   Future<bool> updateElection(int id, String name, String date, String status) async {
    try {
      final response = await http.post(
        Uri.parse('\$baseUrl/edit_election'),
        body: {'name': name, 'election_date': date, 'status': status},
      );
      return response.statusCode == 200;
    } catch (e) {
      print("Error updating election: \$e");
      return false;
    }
  }

   Future<bool> deleteElection(int id) async {
    try {
      final response = await http.delete(Uri.parse('\$baseUrl/delete_electionP'));
      return response.statusCode == 200;
    } catch (e) {
      print("Error deleting election: \$e");
      return false;
    }
  }
