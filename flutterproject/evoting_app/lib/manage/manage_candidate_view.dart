import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ManageCandidatesView extends StatefulWidget {
  const ManageCandidatesView({super.key});

  @override
  _ManageCandidatesViewState createState() => _ManageCandidatesViewState();
}

class _ManageCandidatesViewState extends State<ManageCandidatesView> {
  late Future<List<Map<String, dynamic>>> _candidatesFuture;
  List<Map<String, dynamic>> elections = [];
  String errorMessage = '';
  bool isLoading = true;

  final String baseUrl = "http://192.168.0.27:8000"; // Ensure your server is accessible from your mobile device

  @override
  void initState() {
    super.initState();
    _candidatesFuture = _fetchCandidates();
  }

  Future<List<Map<String, dynamic>>> _fetchCandidates() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/apicandidate"));

      print("Response status: ${response.statusCode}");
      print("Response body: ${response.body}");

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);

        setState(() {
          if (responseData is List) {
            elections = List<Map<String, dynamic>>.from(responseData);
          } else if (responseData is Map<String, dynamic>) {
            elections = [responseData]; // Wrap single object inside a list
          } else {
            errorMessage = 'Unexpected response format';
          }
          isLoading = false;
        });

        return elections
            .where((candidate) {
              final electionStatus = candidate['election_status'] ?? '';
              return electionStatus == 'active' || electionStatus == 'pending';
            })
            .toList();
      } else {
        setState(() {
          errorMessage = 'Failed to load elections';
          isLoading = false;
        });
        throw Exception('Failed to load candidates');
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error fetching candidates: $e';
        isLoading = false;
      });
      throw Exception('Error fetching candidates');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Candidates')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
              ? Center(child: Text(errorMessage))
              : FutureBuilder<List<Map<String, dynamic>>>(
                  future: _candidatesFuture,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    } else if (snapshot.hasError) {
                      return Center(child: Text('Error: ${snapshot.error}'));
                    } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                      return const Center(child: Text('No candidates found.'));
                    }

                    final candidates = snapshot.data!;

                    return Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: DataTable(
                          columns: const [
                            DataColumn(label: Text('#')),
                            DataColumn(label: Text('Name')),
                            DataColumn(label: Text('Position')),
                            DataColumn(label: Text('Election')),
                          ],
                          rows: candidates.map((candidate) {
                            return DataRow(cells: [
                              DataCell(Text(candidate['id']?.toString() ?? 'N/A')),
                              DataCell(Text(candidate['name'] ?? 'N/A')),
                              DataCell(Text(candidate['position'] ?? 'N/A')),
                              DataCell(Text(candidate['election_name'] ?? candidate['election'] ?? 'N/A')),
                            ]);
                          }).toList(),
                        ),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () {
          Navigator.pushNamed(context, '/create_candidate');
        },
      ),
    );
  }
}
