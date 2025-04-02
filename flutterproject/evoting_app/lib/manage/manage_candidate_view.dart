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

  final String baseUrl = "http://192.168.0.27:8000"; 

  @override
  void initState() {
    super.initState();
    _candidatesFuture = _fetchCandidates();
  }

  Future<List<Map<String, dynamic>>> _fetchCandidates() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/candidates/<int:election>"));
      
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        return data
            .where((candidate) {
              final electionStatus = candidate['election_status'] ?? ''; 
              return electionStatus == 'active' || electionStatus == 'pending';
            })
            .map((e) => e as Map<String, dynamic>)
            .toList();
      } else {
        throw Exception('Failed to load candidates');
      }
    } catch (e) {
      print("Error fetching candidates: $e");
      throw Exception('Error fetching candidates');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Candidates')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _candidatesFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text('Error fetching candidates'));
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
                  DataColumn(label: Text('Actions')),
                ],
                rows: candidates.map((candidate) {
                  return DataRow(cells: [
                    DataCell(Text(candidate['id'].toString())),
                    DataCell(Text(candidate['name'] ?? 'N/A')),
                    DataCell(Text(candidate['position'] ?? 'N/A')),
                    DataCell(Text(candidate['election_name'] ?? 'N/A')),
                    DataCell(Row(
                      children: [
                        IconButton(
                          icon: const Icon(Icons.edit, color: Colors.orange),
                          onPressed: () => _editCandidate(candidate),
                        ),
                        IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => _deleteCandidate(candidate['id']),
                        ),
                      ],
                    )),
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

  void _editCandidate(Map<String, dynamic> candidate) {
    // Implement edit candidate functionality
    print("Edit Candidate: ${candidate['name']}");
  }

  void _deleteCandidate(int candidateId) {
    // Implement delete candidate functionality
    print("Delete Candidate ID: $candidateId");
  }
}
