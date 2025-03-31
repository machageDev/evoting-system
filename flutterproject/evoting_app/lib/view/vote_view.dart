import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class VoteView extends StatefulWidget {
  const VoteView({super.key});

  @override
  State<VoteView> createState() => _VoteViewState();
}

class _VoteViewState extends State<VoteView> {
  List elections = [];
  List candidates = [];
  int? selectedElectionId;
  int? selectedCandidateId;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    fetchActiveElections();
  }

  Future<void> fetchActiveElections() async {
    final url = Uri.parse('http://192.168.0.102:8000/api/active_elections');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          elections = jsonDecode(response.body);
        });
      } else {
        showSnackBar("Failed to load elections.");
      }
    } catch (e) {
      showSnackBar("Error: $e");
    }
  }

  Future<void> fetchCandidates(int electionId) async {
    final url = Uri.parse('http://127.168.0.102:8000/api/get_candidates/$electionId');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          candidates = jsonDecode(response.body);
        });
      } else {
        showSnackBar("Failed to load candidates.");
      }
    } catch (e) {
      showSnackBar("Error: $e");
    }
  }

  Future<void> submitVote() async {
    if (selectedCandidateId == null || selectedElectionId == null) {
      showSnackBar("Select an election and a candidate.");
      return;
    }

    setState(() {
      isLoading = true;
    });

    final url = Uri.parse('http://127.168.0.102:8000/api/vote/');
    final token = 'YOUR_USER_TOKEN'; // Replace with token (e.g., SharedPreferences)

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
        body: jsonEncode({
          'candidate_id': selectedCandidateId,
          'election_id': selectedElectionId,
        }),
      );

      if (response.statusCode == 201) {
        showSnackBar("Vote cast successfully!");
        setState(() {
          selectedCandidateId = null; // Reset candidate selection
        });
      } else {
        showSnackBar("Failed to vote: ${response.body}");
      }
    } catch (e) {
      showSnackBar("Error: $e");
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Vote Now")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Select Active Election:",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            DropdownButtonFormField<int>(
              value: selectedElectionId,
              hint: const Text("Choose an Election"),
              onChanged: (int? newElectionId) {
                setState(() {
                  selectedElectionId = newElectionId;
                  selectedCandidateId = null;
                  candidates = [];
                });
                if (newElectionId != null) {
                  fetchCandidates(newElectionId);
                }
              },
              items: elections.map<DropdownMenuItem<int>>((election) {
                return DropdownMenuItem<int>(
                  value: election['id'],
                  child: Text(election['name']),
                );
              }).toList(),
            ),
            const SizedBox(height: 20),
            if (candidates.isNotEmpty)
              const Text(
                "Select Candidate:",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            const SizedBox(height: 10),
            Expanded(
              child: candidates.isEmpty
                  ? const Center(child: Text("No candidates to show."))
                  : ListView.builder(
                      itemCount: candidates.length,
                      itemBuilder: (context, index) {
                        final candidate = candidates[index];
                        return Card(
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundImage: NetworkImage(
                                candidate['profile_picture'].isNotEmpty
                                    ? 'http://127.168.0.54:8000${candidate['profile_picture']}'
                                    : 'https://via.placeholder.com/150',
                              ),
                            ),
                            title: Text(candidate['name']),
                            subtitle: Text(candidate['position']),
                            trailing: Radio<int>(
                              value: candidate['id'],
                              groupValue: selectedCandidateId,
                              onChanged: (value) {
                                setState(() {
                                  selectedCandidateId = value;
                                });
                              },
                            ),
                          ),
                        );
                      },
                    ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: isLoading ? null : submitVote,
                icon: const Icon(Icons.how_to_vote),
                label: isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("Submit Vote"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
