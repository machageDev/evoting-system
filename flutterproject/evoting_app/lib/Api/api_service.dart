import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.0.54:8000';
  static const String loginUrl = '$baseUrl/apilogin';
  static const String registerUrl = '$baseUrl/apiregister';
  static const String electionUrl = '$baseUrl/apielections';
  static const String candidateUrl = '$baseUrl/apicandidates';
  static const String voteUrl = '$baseUrl/apivote';
  static const String resultUrl = '$baseUrl/api_result';
  static const String dashboardUrl ='$baseUrl/api_dashboars';

  // ✅ FETCH DATA FUNCTION
  Future<String> fetchData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/register'));

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
  static Future<Map<String, dynamic>> getVoterDetails(int voterId) async {
    Uri url = Uri.parse('$baseUrl/voter/$voterId/');
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
    Uri url = Uri.parse('$baseUrl/vote/');
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
}

   Future<Map<String, dynamic>> getElectionResults(int electionId, dynamic baseUrl) async {
    final response = await http.get(Uri.parse("$baseUrl/api_result/"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load election results");
    }
  }

 Future<Map<String, dynamic>> fetchDashboardData(String token, dynamic baseUrl) async {
   
    final url = Uri.parse('$baseUrl/dashboard/');

    try {
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token', // If you use token auth, otherwise remove this
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        throw Exception('Failed to load dashboard data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching dashboard data: $e');
    }
  }