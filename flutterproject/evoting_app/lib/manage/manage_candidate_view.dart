
// ignore_for_file: use_build_context_synchronously

import 'package:evoting_app/Api/api_service.dart';
import 'package:flutter/material.dart';




class ManageCandidatesView extends StatefulWidget {
  const ManageCandidatesView({super.key});

  @override
  _ManageCandidatesViewState createState() => _ManageCandidatesViewState();
}

class _ManageCandidatesViewState extends State<ManageCandidatesView> {
  // ignore: unused_field
  final ApiService _apiService = ApiService();  
  late Future<List<Map<String, dynamic>>> _candidatesFuture;

  final String baseUrl = "https://192.168.0.54:8000";
  
  get _ApiService => null; 

  @override
  void initState() {
    super.initState();
    _fetchCandidates();
  }

  void _fetchCandidates() {
    setState(() {
      _candidatesFuture = _ApiService.getCandidates(baseUrl); 
    });
  }

  void _editCandidate(Map<String, dynamic> candidate) {
    TextEditingController nameController =
        TextEditingController(text: candidate['name'] ?? '');
    TextEditingController positionController =
        TextEditingController(text: candidate['position'] ?? '');

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Edit Candidate'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameController, decoration: const InputDecoration(labelText: 'Name')),
              TextField(controller: positionController, decoration: const InputDecoration(labelText: 'Position')),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                await _ApiService.updateCandidate(  
                  candidate['id'],
                  nameController.text,
                  positionController.text,
                  baseUrl,
                );
                _fetchCandidates();
                Navigator.pop(context);
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }

  void _deleteCandidate(int candidateId) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Confirm Deletion'),
          content: const Text('Are you sure you want to delete this candidate?'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                await _ApiService.deleteCandidate(candidateId, baseUrl);  // ✅ Use instance method
                _fetchCandidates();
                Navigator.pop(context);
              },
              child: const Text('Delete'),
            ),
          ],
        );
      },
    );
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
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () {
          Navigator.pushNamed(context, '/createCandidate');
        },
      ),
    );
  }
}
